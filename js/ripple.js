/* CANAL — the canal moves.
   WebGL over the hero photo: a slow shimmer on the reflection, and rings wherever the cursor
   (or a finger) touches the water. Falls back to the plain photo if WebGL isn't available
   or the visitor prefers reduced motion. */
(function () {
  var host = document.querySelector('[data-ripple]');
  if (!host) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var img = host.querySelector('img');
  if (!img) return;

  // Water region of the photo (0-1, top-left origin), and things standing in it to keep still.
  var WATER = (host.getAttribute('data-water') || '0.17,0.6').split(',').map(Number);
  var KEEP = JSON.parse(host.getAttribute('data-keep') || '[]'); // [[x0,y0,x1,y1],...]

  var canvas = document.createElement('canvas');
  canvas.className = 'ripple-canvas';
  var gl = canvas.getContext('webgl', { premultipliedAlpha: false, antialias: false });
  if (!gl) return;

  var MAXR = 12;
  var vs = 'attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}';
  var fs = [
    'precision mediump float;varying vec2 v;uniform sampler2D tex;uniform float t,ca,ia;',
    'uniform vec2 water;uniform vec4 keep[4];uniform vec4 drops[' + MAXR + '];',
    'vec2 cover(vec2 u){if(ca>ia){u.y=(u.y-.5)*(ia/ca)+.5;}else{u.x=(u.x-.5)*(ca/ia)+.5;}return u;}',
    'float box(vec2 u,vec4 b){vec2 a=smoothstep(b.xy-.015,b.xy+.01,u)*(1.-smoothstep(b.zw-.01,b.zw+.015,u));return a.x*a.y;}',
    'void main(){',
    ' vec2 u=cover(v);',
    ' float w=smoothstep(water.x-.03,water.x+.04,u.y)*(1.-smoothstep(water.y-.06,water.y+.02,u.y));',
    ' float k=1.;for(int i=0;i<4;i++){k*=1.-box(u,keep[i]);}w*=k;',
    // ambient shimmer: horizontal wobble like a real reflection
    ' float s=sin(u.y*140.+t*1.6+sin(u.x*7.+t*.6)*2.2)*.0028+sin(u.y*60.-t*.9+u.x*3.)*.0018;',
    ' vec2 d=vec2(s,s*.25)*w;',
    // cursor / touch rings
    ' float hi=0.;',
    ' for(int i=0;i<' + MAXR + ';i++){vec4 r=drops[i];float age=t-r.z;if(r.w<=0.||age<0.||age>3.5)continue;',
    '  vec2 q=(u-r.xy);q.x*=ia;float dist=length(q);',
    '  float wave=sin(dist*95.-age*9.)*exp(-dist*9.)*exp(-age*1.3)*r.w;',
    '  float m=mix(.08,1.,w)*k;d+=normalize(q+1e-5)*wave*.011*m;hi+=wave*.06*m;}',
    ' vec4 c=texture2D(tex,clamp(u+d,0.,1.));',
    ' c.rgb+=hi+s*w*6.;',
    ' gl_FragColor=c;}'
  ].join('\n');

  function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { console.warn(gl.getShaderInfoLog(s)); return null; } return s; }
  var v = sh(gl.VERTEX_SHADER, vs), f = sh(gl.FRAGMENT_SHADER, fs);
  if (!v || !f) return;
  var pr = gl.createProgram(); gl.attachShader(pr, v); gl.attachShader(pr, f); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
  gl.useProgram(pr);

  var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

  var U = {}; ['tex', 't', 'ca', 'ia', 'water', 'keep', 'drops'].forEach(function (n) { U[n] = gl.getUniformLocation(pr, n); });
  var keep = new Float32Array(16); KEEP.slice(0, 4).forEach(function (b, i) { keep.set(b, i * 4); });
  gl.uniform4fv(U.keep, keep);
  gl.uniform2f(U.water, WATER[0], WATER[1]);

  var drops = new Float32Array(MAXR * 4), di = 0, t0 = performance.now();
  function now() { return (performance.now() - t0) / 1000; }
  function addDrop(x, y, s) { drops.set([x, y, now(), s], di * 4); di = (di + 1) % MAXR; }

  var tex = gl.createTexture(), ia = 1.5, ready = false;
  function upload() {
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img); } catch (e) { return; }
    ia = img.naturalWidth / img.naturalHeight; ready = true;
    host.appendChild(canvas); host.classList.add('rippling');
  }
  if (img.complete && img.naturalWidth) upload(); else img.addEventListener('load', upload);

  function size() {
    var dpr = Math.min(window.devicePixelRatio || 1, 1.75);
    var w = host.clientWidth, h = host.clientHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  size(); window.addEventListener('resize', size);

  // map a screen point to image uv (matching the cover crop)
  function toUV(cx, cy) {
    var r = host.getBoundingClientRect(), x = (cx - r.left) / r.width, y = (cy - r.top) / r.height, ca = r.width / r.height;
    if (ca > ia) y = (y - .5) * (ia / ca) + .5; else x = (x - .5) * (ca / ia) + .5;
    return [x, y];
  }
  var last = 0, lx = -1, ly = -1;
  function move(cx, cy, strength) {
    var p = toUV(cx, cy), tn = now();
    if (tn - last < 0.07 && Math.hypot(p[0] - lx, p[1] - ly) < 0.03) return;
    last = tn; lx = p[0]; ly = p[1]; addDrop(p[0], p[1], strength);
  }
  var hero = host.closest('section') || host;
  hero.addEventListener('pointermove', function (e) { move(e.clientX, e.clientY, e.pointerType === 'touch' ? 1 : .8); }, { passive: true });
  hero.addEventListener('pointerdown', function (e) { var p = toUV(e.clientX, e.clientY); addDrop(p[0], p[1], 1.6); }, { passive: true });

  // the odd drop on its own, so it's alive even when nobody's touching it
  setInterval(function () {
    if (document.hidden) return;
    addDrop(.15 + Math.random() * .7, WATER[0] + .05 + Math.random() * (WATER[1] - WATER[0] - .12), .7);
  }, 2600);

  var visible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(host);

  function frame() {
    requestAnimationFrame(frame);
    if (!ready || !visible) return;
    gl.uniform1f(U.t, now());
    gl.uniform1f(U.ca, canvas.width / canvas.height);
    gl.uniform1f(U.ia, ia);
    gl.uniform4fv(U.drops, drops);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  frame();
})();
