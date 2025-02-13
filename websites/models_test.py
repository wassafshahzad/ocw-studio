"""Website models tests"""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from mitol.common.utils import now_in_utc

from websites.constants import WEBSITE_CONFIG_ROOT_URL_PATH_KEY
from websites.factories import (
    WebsiteContentFactory,
    WebsiteFactory,
    WebsiteStarterFactory,
)
from websites.site_config_api import SiteConfig

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ("metadata", "markdown", "dirpath", "exp_checksum"),
    [
        [  # noqa: PT007
            {"my": "metadata"},
            "# Markdown",
            None,
            "519b0f9225d269b6f2fe3636c8ef6d0de4c9fd8fde30990fb8a1c65c4575f3ae",
        ],
        [  # noqa: PT007
            {"my": "metadata"},
            None,
            "path/to",
            "a6ffb383023705e862b9357c23155252808722a62a3effa7c0826a0918095a19",
        ],
        [  # noqa: PT007
            None,
            "# Markdown",
            "path/to",
            "9323949f05768fb0a69ceb96eecb6bf040681fa17102fb93f33ee56493d8b41e",
        ],
    ],
)
def test_websitecontent_calculate_checksum(metadata, markdown, dirpath, exp_checksum):
    """Verify calculate_checksum() returns the expected sha256 checksum"""
    content = WebsiteContentFactory.build(
        markdown=markdown,
        metadata=metadata,
        dirpath=dirpath,
        filename="myfile",
        type="mytype",
        title="My Title",
    )
    # manually computed checksum in a python shell
    assert content.calculate_checksum() == exp_checksum


@pytest.mark.parametrize("has_file_widget", [True, False])
@pytest.mark.parametrize("has_file", [True, False])
@pytest.mark.parametrize("is_video", [True, False])
@pytest.mark.parametrize("has_metadata", [True, False])
@pytest.mark.parametrize("transcript_value", [None, "", "transcript.pdf"])
def test_websitecontent_full_metadata(
    has_file_widget, has_file, is_video, has_metadata, transcript_value
):
    """WebsiteContent.full_metadata returns expected file field in metadata when appropriate"""
    file = SimpleUploadedFile("test.txt", b"content")
    title = ("Test Title",)
    description = "Test Description"
    config_fields = [
        {"label": "Description", "name": "description", "widget": "text"},
        {"label": "My File", "name": "my_file", "widget": "file", "required": False},
    ]
    fields = config_fields if has_file_widget else config_fields[0:1]
    if is_video and has_metadata:
        fields.append(
            {
                "fields": [
                    {
                        "label": "Video Captions (WebVTT) URL",
                        "name": "video_captions_file",
                        "widget": "string",
                    },
                    {
                        "label": "Video Transcript (PDF) URL",
                        "name": "video_transcript_file",
                        "widget": "string",
                    },
                ],
                "label": "Video Files",
                "name": "video_files",
                "widget": "object",
            }
        )
    metadata = {"title": title, "description": description}
    meta_val = (
        f"/sites/mysite/{transcript_value}.webvtt"
        if transcript_value
        else transcript_value
    )
    if is_video and has_metadata:
        metadata["video_files"] = {
            "video_captions_file": meta_val,
            "video_transcript_file": meta_val,
        }
    content = WebsiteContentFactory.build(
        type="resource",
        metadata=metadata if has_metadata else None,
        file=(file if has_file else None),
        website=WebsiteFactory(
            starter=WebsiteStarterFactory.create(
                config={
                    "content-dir": "content",
                    "root-url-path": "sites",
                    "collections": [
                        {
                            "name": "resource",
                            "label": "Resource",
                            "category": "Content",
                            "folder": "content/resource",
                            "fields": fields,
                        }
                    ],
                }
            ),
            url_path="sites/mysite-fall-2008",
            name="mysite",
        ),
    )
    expected_val = (
        f"/{content.website.url_path}/{transcript_value}.webvtt"
        if transcript_value
        else transcript_value
    )

    full_metadata = content.full_metadata
    if has_metadata:
        assert full_metadata["title"] == title
        assert full_metadata["description"] == description

    if has_file_widget:
        assert full_metadata["my_file"] == (
            content.file.url.replace(content.website.s3_path, content.website.url_path)
            if has_file
            else None
        )
    elif has_metadata:
        assert "my_file" not in full_metadata

    if is_video and has_metadata:
        assert full_metadata["video_files"]["video_captions_file"] == expected_val
        assert full_metadata["video_files"]["video_transcript_file"] == expected_val
    if not has_metadata and not has_file_widget:
        assert full_metadata is None


def test_website_starter_unpublished():
    """Website should set has_unpublished_live and has_unpublished_draft if the starter is updated"""
    website = WebsiteFactory.create(
        has_unpublished_live=False, has_unpublished_draft=False
    )
    second_website = WebsiteFactory.create(
        has_unpublished_live=False, has_unpublished_draft=False, starter=website.starter
    )
    website.starter.save()
    website.refresh_from_db()
    assert website.has_unpublished_draft is True
    assert website.has_unpublished_live is True
    second_website.refresh_from_db()
    assert second_website.has_unpublished_draft is True
    assert second_website.has_unpublished_live is True


def test_website_content_unpublished():
    """Website should set has_unpublished_live and has_unpublished_draft if any related content is updated"""
    website = WebsiteFactory.create()
    content = WebsiteContentFactory.create(website=website)
    website.has_unpublished_live = False
    website.has_unpublished_draft = False
    website.save()
    other_content = WebsiteContentFactory.create()
    other_content.save()
    website.refresh_from_db()
    # website should not have changed since the content is for a different website
    assert website.has_unpublished_live is False
    assert website.has_unpublished_draft is False
    content.save()
    website.refresh_from_db()
    assert website.has_unpublished_live is True
    assert website.has_unpublished_draft is True


@pytest.mark.parametrize(
    ("name", "root_url", "is_home", "version", "expected_path"),
    [
        ["test-course", "courses", False, "live", "courses/test-course"],  # noqa: PT007
        ["ocw-home-page", "", True, "draft", ""],  # noqa: PT007
    ],
)
def test_website_get_full_url(  # noqa: PLR0913
    settings, name, root_url, is_home, version, expected_path
):  # pylint:disable=too-many-arguments
    """Verify that Website.get_full_url returns the expected value"""
    settings.OCW_STUDIO_LIVE_URL = "http://test-live.edu"
    settings.OCW_STUDIO_DRAFT_URL = "http://test-draft.edu"
    expected_domain = (
        settings.OCW_STUDIO_LIVE_URL
        if version == "live"
        else settings.OCW_STUDIO_DRAFT_URL
    )
    starter = WebsiteStarterFactory.create()
    starter.config["root-url-path"] = root_url
    starter.save()
    settings.ROOT_WEBSITE_NAME = name if is_home else "test-home"
    website = WebsiteFactory.create(name=name, starter=starter, url_path=expected_path)
    assert website.get_full_url(version) == "/".join(
        section for section in [expected_domain, expected_path] if section
    )


def test_website_get_full_url_no_starter():
    """Verify that Website.get_full_url returns None if there is no starter"""
    website = WebsiteFactory.create(starter=None)
    assert website.get_full_url("draft") is None
    assert website.get_full_url("live") is None


@pytest.mark.parametrize(
    ("name", "root_url", "expected_path"),
    [
        ["test-course-1", "courses", "courses/test-course-1"],  # noqa: PT007
        ["test-course-2", "sites", "sites/test-course-2"],  # noqa: PT007
        ["test-course-3", "", "test-course-3"],  # noqa: PT007
    ],
)
def test_website_s3_path(name, root_url, expected_path):
    """The correct s3 path should be returned for a site"""
    starter = WebsiteStarterFactory.create(config={"root-url-path": root_url})
    website = WebsiteFactory.create(name=name, starter=starter)
    assert website.s3_path == expected_path


def test_website_url_path_from_metadata_no_starter():
    """None should be returned for a site without a starter"""
    assert WebsiteFactory.build(starter=None).url_path_from_metadata() is None


def test_website_url_path_from_metadata_no_format():
    """Website.name should be returned for a site without site-url-format in starter config"""
    starter = WebsiteStarterFactory.create(
        config={WEBSITE_CONFIG_ROOT_URL_PATH_KEY: "sites"}
    )
    website = WebsiteFactory.build(starter=starter)
    assert website.url_path_from_metadata() == website.name


def test_website_url_path_from_metadata_published(ocw_site):
    """Website.name should be returned for a that's already been published"""
    ocw_site.publish_date = now_in_utc()
    assert ocw_site.url_path_from_metadata() == ocw_site.name


@pytest.mark.parametrize(
    "missing_keys", [[], ["course_nr", "year"], ["term"], ["title", "year"]]
)
def test_website_url_path_from_metadata(missing_keys):
    """The expected url should be returned based on starter config format and supplied metadata"""
    metadata = {
        "course_nr": "1.1",
        "title": "My Course",
        "term": "Fall",
        "year": "2025",
    }
    for key in missing_keys:
        metadata.pop(key)
    starter = WebsiteStarterFactory.create(
        config={
            "site-url-format": "[meta:course_nr]-[meta:title]-[meta:term]-[meta:year]"
        }
    )
    website = WebsiteFactory.create(starter=starter, not_published=True)
    course_nr = "1-1" if metadata.get("course_nr") is not None else "[meta:course_nr]"
    title = "my-course" if metadata.get("title") is not None else "[meta:title]"
    term = "fall" if metadata.get("term") is not None else "[meta:term]"
    year = metadata.get("year", "[meta:year]")
    expected_url_path = f"{course_nr}-{title}-{term}-{year}"
    assert website.url_path_from_metadata(metadata) == expected_url_path


@pytest.mark.parametrize("root_path", ["", "courses", "sites"])
@pytest.mark.parametrize("url_path", ["", "my-site", "other-site-fall-2024"])
def test_assemble_full_url_path(root_path, url_path):
    """assemble_full_url_path should combine the root url path and site url path"""
    website = WebsiteFactory.create(
        starter=WebsiteStarterFactory(
            config={WEBSITE_CONFIG_ROOT_URL_PATH_KEY: root_path}
        )
    )
    assert website.assemble_full_url_path(url_path) == f"{root_path}/{url_path}".strip(
        "/"
    )


@pytest.mark.parametrize(
    "url_path", [None, "courses/1-1-my-site-fall-2019", "courses/2-2-my-site-fall-2049"]
)
@pytest.mark.parametrize("with_prefix", [True, False])
@pytest.mark.parametrize("published", [True, False])
def test_get_url_path(ocw_site, url_path, with_prefix, published):
    """get_url_path should return the expected url path with or without a prefix"""
    ocw_site.publish_date = now_in_utc() if published else None
    ocw_site.url_path = url_path
    config = SiteConfig(ocw_site.starter.config)
    root_path = config.root_url_path
    if url_path is None and published:
        site_path = ocw_site.name
    else:
        site_path = (
            (url_path or config.site_url_format).replace(root_path, "").strip("/")
        )
    assert ocw_site.get_url_path(with_prefix=with_prefix) == (
        f"{config.root_url_path}/{site_path}" if with_prefix else site_path
    )


@pytest.mark.parametrize(
    "path",
    ["https://github.com/org/repo/starter1", "https://github.com/org/repo/starter2"],
)
def test_ocw_hugo_projects_url(path):
    """The ocw_hugo_projects_url property should return the proper git repo URL"""
    starter = WebsiteStarterFactory(path=path)
    assert starter.ocw_hugo_projects_url == "https://github.com/org/repo.git"
