function Boid(t,i){this.id=Boid.lastId++,this.position=[t,i],this.size=5,this.color="#CAB19D",this.velocity=[25-50*Math.random(),25-50*Math.random()]}function vDiff(t,i){return[t[0]-i[0],t[1]-i[1]]}function vLength(t){return Math.sqrt(t[0]*t[0]+t[1]*t[1])}function round(t){return.5+t|0}function draw(t){var i=(t-(lastTimestamp||t))/1e3;lastTimestamp=t,context.clearRect(0,0,canvas.width,canvas.height);for(var o=0;o<maxPoolSize;o++){var n=pool[o];n.update(i),n.draw()}window.requestAnimFrame(draw)}var canvas=document.createElement("canvas"),context=canvas.getContext("2d"),pool=[],maxPoolSize=10,distanceThreshold=80,lastTimestamp=0,nodeConnections=[];canvas.width=window.innerWidth,canvas.height=700,canvas.id="core-bg",maxPoolSize=canvas.width*canvas.height/35e3,Boid.lastId=0,Boid.prototype={update:function(t){for(var i=0;i<maxPoolSize;i++){var o=pool[i],n=this.distanceTo(o);n<distanceThreshold&&(cohesion=[])}this.position[0]+=this.velocity[0]*t,this.position[1]+=this.velocity[1]*t,this.position[0]>canvas.width&&(this.position[0]=0),this.position[1]>canvas.height&&(this.position[1]=0),this.position[0]<0&&(this.position[0]=canvas.width),this.position[1]<0&&(this.position[1]=canvas.height)},distanceTo:function(t){var i=vDiff(this.position,t.position);return Math.abs(vLength(i))},isConnectedTo:function(t){return nodeConnections[t.id]==this.id||nodeConnections[this.id]==t.id},connectTo:function(t){nodeConnections[this.id]=t.id,nodeConnections[t.id]=this.id},draw:function(){var t=[round(this.position[0]),round(this.position[1])],i=0;context.globalAlpha=.1;for(var o=0;o<maxPoolSize;o++){var n=pool[o],e=this.distanceTo(n),a=1-e/distanceThreshold;e<=distanceThreshold&&(i++,this.isConnectedTo(n)||(this.connectTo(n),context.beginPath(),context.moveTo(t[0],t[1]),context.lineTo(round(n.position[0]),round(n.position[1])),context.stroke()))}context.globalAlpha=.5,context.beginPath(),context.arc(t[0],t[1],this.size*(i/5),0,2*Math.PI),context.fillStyle="#CAB19D",context.fill()}},window.requestAnimFrame=function(){return window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||function(t,i){window.setTimeout(t,1e3/60)}}();for(var i=0;i<maxPoolSize;i++)pool.push(new Boid(Math.random()*canvas.width,Math.random()*canvas.height));$("#product-core > .detail").append(canvas),window.requestAnimFrame(draw);