import EssentialsPlugin from "@ckeditor/ckeditor5-essentials/src/essentials"
import AutoformatPlugin from "@ckeditor/ckeditor5-autoformat/src/autoformat"
import BoldPlugin from "@ckeditor/ckeditor5-basic-styles/src/bold"
import ItalicPlugin from "@ckeditor/ckeditor5-basic-styles/src/italic"
import UnderlinePlugin from "@ckeditor/ckeditor5-basic-styles/src/underline"
import BlockQuotePlugin from "@ckeditor/ckeditor5-block-quote/src/blockquote"
import HeadingPlugin from "@ckeditor/ckeditor5-heading/src/heading"
import ImagePlugin from "@ckeditor/ckeditor5-image/src/image"
import ImageCaptionPlugin from "@ckeditor/ckeditor5-image/src/imagecaption"
import ImageStylePlugin from "@ckeditor/ckeditor5-image/src/imagestyle"
import ImageToolbarPlugin from "@ckeditor/ckeditor5-image/src/imagetoolbar"
import LinkPlugin from "@ckeditor/ckeditor5-link/src/link"
import ListPlugin from "@ckeditor/ckeditor5-list/src/list"
import ParagraphPlugin from "@ckeditor/ckeditor5-paragraph/src/paragraph"

import Markdown from "./plugins/Markdown"
import ResourceEmbed from "./plugins/ResourceEmbed"
import ResourcePicker from "./plugins/ResourcePicker"
import { ADD_RESOURCE } from "./plugins/constants"
import ResourceLink from "./plugins/ResourceLink"

export const FullEditorConfig = {
  plugins: [
    EssentialsPlugin,
    AutoformatPlugin,
    BoldPlugin,
    ItalicPlugin,
    UnderlinePlugin,
    BlockQuotePlugin,
    HeadingPlugin,
    ImagePlugin,
    ImageCaptionPlugin,
    ImageStylePlugin,
    ImageToolbarPlugin,
    LinkPlugin,
    ListPlugin,
    ParagraphPlugin,
    ResourceEmbed,
    ResourcePicker,
    ResourceLink,
    Markdown
  ],
  toolbar: {
    items: [
      "heading",
      "|",
      "bold",
      "italic",
      "underline",
      "link",
      "bulletedList",
      "numberedList",
      "blockQuote",
      "undo",
      "redo",
      ADD_RESOURCE
    ]
  },
  image: {
    toolbar: ["imageStyle:full", "imageStyle:side", "|", "imageTextAlternative"]
  },
  language: "en"
}

export const MinimalEditorConfig = {
  plugins: [
    EssentialsPlugin,
    AutoformatPlugin,
    BoldPlugin,
    ItalicPlugin,
    UnderlinePlugin,
    BlockQuotePlugin,
    LinkPlugin,
    ListPlugin,
    ParagraphPlugin,
    Markdown
  ],
  toolbar: {
    items: [
      "bold",
      "italic",
      "underline",
      "link",
      "bulletedList",
      "numberedList",
      "blockQuote",
      "undo",
      "redo"
    ]
  },
  language: "en"
}
