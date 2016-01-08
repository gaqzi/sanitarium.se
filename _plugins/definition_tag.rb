module Jekyll
  module DefinitionFilter
    def define(word)
      "<defn title=\"#{@context['page']['definitions'][word]}\">#{word}</defn>"
    end
  end
end

Liquid::Template.register_filter(Jekyll::DefinitionFilter)
