require 'digest'
require 'liquid'
require 'tempfile'

module Jekyll
  module RenderBannerFilter
    def render_banner(page)
      banner = Banner.new(page)
      banner.create! unless banner.exists?

      "/#{banner.path}"
    end

    class Banner
      def initialize(page)
        @page = page
      end

      def checksum
        @checksum ||= begin
          md5 = Digest::MD5.new
          md5 << "#{@page['date']}--#{@page['title']}--#{@page['subtitle']}"
          md5.hexdigest
        end
      end

      def exists?
        not Dir[path].empty?
      end

      def path
        "#{banner_path}/#{@page['slug']}--#{checksum}.gen.png"
      end

      def phantomjs_command(input_file, output_file, dimensions = '1200px*630px')
        "#{phantomjs} #{rasterize} #{input_file} #{output_file} '#{dimensions}'"
      end

      def create!
        template = Liquid::Template.parse(File.open(template_file).read)
        file = Tempfile.new([checksum, '.html'])
        file.write(template.render(@page))
        file.close
        puts "banner: #{@page['title']}"

        output = `#{phantomjs_command(file.path, path)} >&1`
        raise "Failed to create banner! '#{output}'" unless $?.exitstatus == 0
      end

      private
      def banner_path
        'img/banners'
      end

      def template_file
        '_layouts/banner.html'
      end

      def phantomjs
        'node_modules/phantomjs-prebuilt/bin/phantomjs'
      end

      def rasterize
        '_rasterize.js'
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::RenderBannerFilter)
