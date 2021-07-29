import SiteContentEmbed from "./SiteContentEmbed"
import Markdown from "./Markdown"
import { createTestEditor, markdownTest } from "./test_util"
import { turndownService } from "../turndown"

const getEditor = createTestEditor([SiteContentEmbed, Markdown])

describe("SiteContentEmbed plugin", () => {
  afterEach(() => {
    turndownService.rules.array = turndownService.rules.array.filter(
      (rule: any) => rule.filter !== "figure"
    )
    // @ts-ignore
    turndownService._customRulesSet = undefined
  })

  it("should take in and return 'resource' shortcode", async () => {
    const editor = await getEditor("{{< resource 1234567890 >}}")
    // @ts-ignore
    expect(editor.getData()).toBe("{{< resource 1234567890 >}}")
  })

  it("should serialize to and from markdown", async () => {
    const editor = await getEditor("")
    markdownTest(
      editor,
      "{{< resource asdfasdfasdfasdf >}}",
      `<section>asdfasdfasdfasdf</section>`
    )
  })
})
