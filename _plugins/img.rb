module Jekyll
  class ImageTag < Liquid::Tag
    ALT_TEXT = /(alt="([^"]+)")/
    LAZY = /(lazy=(true|false))/

    def initialize(tag_name, text, parse_context)
      super
      @alt = ""
      if text =~ ALT_TEXT
        @alt = "alt=\"#{$2}\" title=\"#{$2}\""
        text.slice!($1)
      end
      @lazy = 'loading="lazy"'
      if text =~ LAZY
        @lazy = '' if $2 != 'true'
        text.slice!($1)
      end

      @src = text.strip
    end

    def render(context)
      "<img class=\"center-block img-responsive\" #{@lazy} #{@alt} src=\"#{@src}\">"
    end
  end
end

Liquid::Template.register_tag("img", Jekyll::ImageTag)
