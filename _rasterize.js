var page = require('webpage').create(),
  system = require('system'),
  address, output, size;

if (system.args.length < 3 || system.args.length > 5) {
  console.log('Usage: rasterize.js URL filename [paperwidth*paperheight|paperformat] [zoom]');
  console.log('  paper (pdf output) examples: "5in*7.5in", "10cm*20cm", "A4", "Letter"');
  phantom.exit(1);
} else {
  address = system.args[1];
  output = system.args[2];
  page.viewportSize = { width: 600, height: 600 };
  if (system.args.length > 3 && system.args[2].substr(-4) === ".pdf") {
    size = system.args[3].split('*');
    page.paperSize = size.length === 2 ? { width: size[0], height: size[1], margin: '0px' }
      : { format: system.args[3], orientation: 'portrait', margin: '1cm' };
  }
  if (system.args.length > 4) {
    page.zoomFactor = system.args[4];
  }

  // Thank you, https://gist.github.com/cjoudrey/1341747
  var renderTimeout,
      forcedRenderTimeout,
      count = 0,
      resourceWait  = 300,
      maxRenderWait = 10000;

  function doRender() {
    page.render(output);
    phantom.exit();
  }

  page.onResourceRequested = function (req) {
    count += 1;
    console.log('> ' + req.id + ' - ' + req.url);
    clearTimeout(renderTimeout);
  };

  page.onResourceReceived = function (res) {
    if (!res.stage || res.stage === 'end') {
      count -= 1;
      console.log(res.id + ' ' + res.status + ' - ' + res.url);
      if (count === 0) {
        renderTimeout = setTimeout(doRender, resourceWait);
      }
    }
  };

  page.open(address, function (status) {
    if (status !== 'success') {
      console.log('Unable to load the address!');
      phantom.exit();
    } else {
      forcedRenderTimeout = setTimeout(function () {
        console.log(count);
        doRender();
      }, maxRenderWait);
    }
  });
}
