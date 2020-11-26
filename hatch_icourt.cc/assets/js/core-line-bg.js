  var canvas = document.createElement('canvas')
    , context = canvas.getContext('2d')
    , pool = []
    , maxPoolSize = 10
    , distanceThreshold = 80
    , lastTimestamp = 0
    , nodeConnections = []
  ;

  // document.getElementById('products').appendChild(canvas);
  canvas.width = window.innerWidth;
  canvas.height = 700;
  canvas.id = 'core-bg';
  maxPoolSize = ( canvas.width * canvas.height ) / 35000

  function Boid(x,y) {
    this.id = Boid.lastId++;
    this.position = [x, y];
    this.size = 5;
    this.color = "#CAB19D";
    this.velocity = [25-Math.random()*50, 25-Math.random()*50];
  };

  Boid.lastId = 0;

  Boid.prototype = {
    update: function(dt) {
      for (var i = 0; i < maxPoolSize; i++) {
        var boid = pool[i]
          , distance = this.distanceTo(boid)
        ;
        if(distance < distanceThreshold) {
          cohesion = []
        }
      };

      this.position[0] += this.velocity[0] * dt;
      this.position[1] += this.velocity[1] * dt;

      if(this.position[0] > canvas.width) {
        this.position[0] = 0;
        // this.velocity[0] *= -1;
      }

      if(this.position[1] > canvas.height) {
        this.position[1] = 0;
        // this.velocity[1] *= -1;
      }

      if(this.position[0] < 0) {
        this.position[0] = canvas.width;
        // this.velocity[0] *= -1;
      }
      if(this.position[1] < 0) {
        this.position[1] = canvas.height;
        // this.velocity[1] *= -1;
      };
    },

    distanceTo: function(boid) {
      var diff = vDiff(this.position, boid.position);
      return Math.abs(vLength(diff));
    },

    isConnectedTo: function(boid) {
      return nodeConnections[boid.id] == this.id
          || nodeConnections[this.id] == boid.id;
    },

    connectTo: function(boid) {
      nodeConnections[this.id] = boid.id;
      nodeConnections[boid.id] = this.id;
    },

    draw: function() {
      var pos = [round(this.position[0]), round(this.position[1])]
        , connections = 0;
      context.globalAlpha = 0.1;
      for (var i = 0; i < maxPoolSize; i++) {
        var boid = pool[i]
          , distance = this.distanceTo(boid)
          , opacity = 1-( distance/distanceThreshold )
        ;
        if(distance <= distanceThreshold) {
          connections++;
          if(!this.isConnectedTo( boid )){
            this.connectTo(boid);
            context.beginPath();
            context.moveTo( pos[0], pos[1]);
            context.lineTo(round( boid.position[0] ), round( boid.position[1] ));
            context.stroke();
          }
        }
      };
      context.globalAlpha = 0.5;

      context.beginPath();
      context.arc(
        pos[0],
        pos[1],
        this.size*( connections/5 ),
        0, Math.PI*2
      );
      context.fillStyle = '#CAB19D';
      context.fill();


    }
  };

  function vDiff(a, b) {
    return [ a[0] - b[0], a[1] - b[1] ];
  }

  function vLength(a) {
    return Math.sqrt( ( a[0]*a[0] ) + (a[1]*a[1]) );
  }

  function round(i) { return 0.5 + i | 0 }
  function draw(timestamp) {
    var dt = ( timestamp - (lastTimestamp || timestamp) ) / 1000;
    lastTimestamp = timestamp;

    context.clearRect(0,0,canvas.width, canvas.height);

    for (var i = 0; i < maxPoolSize; i++) {
      var boid = pool[i];
      boid.update(dt);
      boid.draw();
    }

    window.requestAnimFrame(draw);
  }

  window.requestAnimFrame = (function(){ return  window.requestAnimationFrame       || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame    || window.oRequestAnimationFrame      || window.msRequestAnimationFrame     || function(/* function */ callback, /* DOMElement */ element){ window.setTimeout(callback, 1000 / 60); }; })();

      for (var i = 0; i < maxPoolSize; i++) {
        pool.push(
          new Boid(Math.random()*canvas.width, Math.random()*canvas.height)
        );
      }
      // document.body.appendChild(canvas);
      $('#product-core > .detail').append(canvas);
      window.requestAnimFrame(draw);