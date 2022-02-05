module Jekyll
  class ImageTag < Liquid::Tag
    ALT_TEXT = /(alt="([^"]+)")/

    def initialize(tag_name, text, parse_context)
      super
      @alt = ""
      if text =~ ALT_TEXT
        @alt = "alt=\"#{$2}\" title=\"#{$2}\""
        text.slice!($1)
      end

      @src = text.strip
    end

    def render(context)
      "<img class=\"center-block img-responsive\" #{@alt} src=\"#{@src}\">"
    end
  end
end

Liquid::Template.register_tag("img", Jekyll::ImageTag)
