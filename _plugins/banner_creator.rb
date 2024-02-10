require 'digest'
require 'liquid'
require 'net/http'
require 'tempfile'
require 'webrick'

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
        # file = Tempfile.new([checksum, '.html'])
        dir = Dir.mktmpdir("banner")
        file = File.new(File.join(dir, "#{checksum}.html"), "w+")
        file.write(template.render(@page))
        file.close
        puts "banner: #{@page['title']} - #{file.path} - #{path}"

        # Run webrick in a thread so it can execute at the same time as the rest of this
        webrick = Thread.new do
          server = WEBrick::HTTPServer.new Port: 3001, DocumentRoot: dir
          trap('INT') { server.shutdown }
          server.start
        end

        server_path = ERB::Util.url_encode("http://jekyll:3001/#{checksum}.html")

        # assume this will be running in docker compose since we need the screenshotting service now
        uri = URI("http://ws-screenshot:3000/api/screenshot?resX=1200&resY=630&outFormat=png&waitTime=150&isFullPage=false&dismissModals=false&url=#{server_path}")
        Net::HTTP.start(uri.host, uri.port) do |http|
          http.open_timeout = 0.5 # how long to wait for the docker network to be available
          http.read_timeout = 40 # how long we'll wait for a response in total
          req = Net::HTTP::Get.new uri
          puts req.uri

          http.request req do |response|
            raise "Failed create banner: #{response.message}" unless response.code == "200"

            File.open(path, "w+") do |f|
              response.read_body { |chunk| f.write chunk }
            end
          end
        end

        webrick.kill
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
