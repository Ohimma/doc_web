$(function() {

	$('.event-detail').find('.prev').each(function(){
		$(this).css('left',$('#logo').offset().left - 80 + 'px');
	});

	$('.event-detail').find('.next').each(function(){
		$(this).css('left',$('#logo').offset().left + 1050 + 'px');
	});

	$(window).scroll(function() {
	  // console.log($('body').scrollTop());
	  if($('body').scrollTop() > 650){
	  	$('#header').addClass('bg');
	  } else {
	  	$('#header').removeClass('bg');
	  }
	});

	$('#logo').click(function(){
		$('body').attr('class','');
		var productPager = $('#products > .slidesjs-pagination').find('a');
		productPager[0].click();
		$('body').animate({scrollTop: 0}, 500);
		return false;
	});

	$('#nav2-event').click(function(){
		$('body').animate({scrollTop: $('#event').offset().top}, 500);
		return false;
	});

	$('#nav2-product').click(function(){
		var productPager = $('#products > .slidesjs-pagination').find('a');
		productPager[0].click();
		$('body').attr('class','show-product active-1');
		$('body').animate({scrollTop: 0}, 500);
		return false;
	});

	// Init Core lines
	function initCoreLines() {
		var coreLines = $('#core-lines');
		var ctx = coreLines[0].getContext("2d");
		ctx.translate(0.5, 0.5)
		ctx.lineWidth = 1;
		ctx.strokeStyle="#D7D7D7";
		ctx.moveTo(360.5,123.5); // 核心业务能力
		ctx.lineTo(470.5,103.5); // 市场开拓能力
		ctx.lineTo(585.5,169.5); // 法律新技术能力
		ctx.lineTo(565.5,268.5); // 必备技术
		ctx.lineTo(500.5,322.5); // 工具方法
		ctx.lineTo(400.5,303.5); // 获取资源
		ctx.lineTo(299.5,343.5); // 降低成本
		ctx.lineTo(230.5,255.5); // 提高效率
		ctx.lineTo(240.5,132.5); // 自身价值
		ctx.lineTo(360.5,123.5); // 核心业务能力
		ctx.stroke();

		ctx.moveTo(360.5,123.5);
		ctx.lineTo(230.5,255.5);
		ctx.lineTo(565.5,268.5);
		ctx.lineTo(470.5,103.5);
		ctx.lineTo(400.5,303.5);
		ctx.lineTo(240.5,132.5);
		ctx.lineTo(585.5,169.5);
		ctx.lineTo(400.5,303.5);
		ctx.lineTo(360.5,123.5);
		ctx.lineTo(299.5,343.5);
		ctx.strokeStyle="#E7E7E7";
		ctx.stroke();
	}
	initCoreLines();

	// show product
	function showProduct(id) {
		$('body').attr('class','show-product active-' + id);
	}

	$('.show-product').click(function(event){
		var productId = $(this).attr('rel');
		showProduct(productId);
	});

	// Close Product
	$('#close-product').click(function(){
		$('body').attr('class','');
	});


	$('#product-nav').find('a').click(function(event){
		var productPager = $('#products > .slidesjs-pagination').find('a');
		var targetProduct = $(this).attr('rel');
		console.log('show product' + $(this).attr('rel'));
		productPager[targetProduct-1].click();
		$('body').attr('class','show-product active-' + targetProduct);
	});

	
  $('#products').slidesjs({
    width: 100,
    height: 700,
    callback: {
      loaded: function(number) {
        // Use your browser console to view log
        console.log('SlidesJS: Loaded with slide #' + number);

        // Show start slide in log
        $('#slidesjs-log .slidesjs-slide-number').text(number);
      },
      start: function(number) {
        // Use your browser console to view log
        console.log('SlidesJS: Start Animation on slide #' + number);
      },
      complete: function(number) {
        if($('body').hasClass('show-product')){
        	$('body').attr('class','show-product active-' + number);
        }
        $('#slidesjs-log .slidesjs-slide-number').text(number);
        // $('#alpha-video').get(0).play();
      }
    }
  });

  $('.video-thumb').click(function(event){
  	$('body').attr('class','');
  	var videoID = $(this).attr('rel');
  	$('#usa-video-' + videoID + '').show();
  	$('#cinema').removeClass('hide-cimema').addClass('show');
  	$('#usa-video-' + videoID + '_html5_api').get(0).play();
  });
  $('#close-video').click(function(){
  	$('#cinema').removeClass('show').addClass('hide-cimema');
  	setTimeout(function(){
  		$('#cinema').removeClass('hide-cimema');
  	},400);
  	$('#usa-video-1').hide();
  	$('#usa-video-2').hide();
  	$('#usa-video-1_html5_api').get(0).pause();
  	$('#usa-video-2_html5_api').get(0).pause();
  });

  // -------------------------------------
  // Events ******************************
  // -------------------------------------

  var EventArea = $('#event')

  // Gernerate Photos background
  var EventPhotos = $('#event-photos');
  var EventPhotoItem;
  for(i=0;i<32;i++) {
  	var Photos = [
  		'2-1','2-2','2-3','1-1','1-2','1-3','1-6','1-7','1-8','1-9','1-10','1-14','1-15','1-16',
  		'1-4','1-5','2-6','2-7','2-8','1-11','1-12','1-13',
  		'3-1','3-2','3-3','3-4','3-5','2-4','2-5','3-6','3-7','3-8','3-9','2-9','2-10','2-11'
  	];
  	var Category = '';
  	if ($.inArray(i,[2,13,16,28]) >= 0) { Category = 'event-1 '; }
  	if ($.inArray(i,[4,10,15,27]) >= 0) { Category = 'event-2 '; }
  	if ($.inArray(i,[6,18,23,29]) >= 0) { Category = 'event-3 '; }
  	// console.log(Category);
  	EventPhotoItem = $('<li class="' + Category + 'event-photo-' + i + '" style="background-image:url(\'assets/images/events/thumb/' + Photos[i] + '.jpg\')"><span>' + i + '</span></li>');
  	EventPhotoItem.appendTo(EventPhotos);
  }

  // Add click event for event buttons
  $('#event-buttons').children().each(function(index){
  	$(this).mouseover(function(){
  		$('#event-photos li:not(.event-' + (index + 1) + ')').addClass('backward');
  		$('#event-photos li.event-' + (index + 1) + '').addClass('forward');
  	});
  	$(this).mouseout(function(){
  		$('#event-photos li').removeClass('backward').removeClass('forward');
  	});
  	$(this).click(function(){
  		$('#event-photos li').removeClass('backward').removeClass('forward');
  		var Timeline = $('#event-detail-' + (index+1) );
  		Timeline.addClass('show');
  	});
  });

  // Init event timelines
  function getRandomIntInclusive(min, max) {
	  min = Math.ceil(min);
	  max = Math.floor(max);
	  return Math.floor(Math.random() * (max - min + 1)) + min;
	}
  $('.event-detail').each(function(index){
  	var timelineID = index+1;
  	var buttonClose = $(this).children('.close');
  	buttonClose.each(function(){
  		$(this).click(function(){
  			$('.event-detail').removeClass('show');
  			var Timeline = $('#timeline-' + timelineID);
  			Timeline.attr('rel', '0');
  			Timeline.css('transform','translate3d(0,0,0)');
  		});
  	});
  	var buttonPrev = $(this).children('.prev');
  	buttonPrev.each(function(){
  		$(this).click(function(){
	  		var stepSize = 240;
		  	var totalStep = 2;
		  	if(timelineID=='1'){
		  		totalStep = 4;
		  	}
		  	var Timeline = $('#timeline-' + timelineID);
		  	// console.log(Timeline);
		  	var currentPos = Timeline.attr('rel');
		  	console.log(currentPos);
		  	if ( currentPos > 0 ) {
			  	var targetPos = parseInt(currentPos) - 1;
			  	console.log('goto pos ' + targetPos);
			  	Timeline.attr('rel', targetPos);
			  	Timeline.css('transform','translate3d(-'+ stepSize * targetPos * 4 +'px,0,0)');
			  }
			  else {
			  	Timeline.attr('rel','0');
			  	Timeline.css('transform','');
			  }
	  	});
  	});
  	var buttonNext = $(this).children('.next');
  	buttonNext.each(function(){
  		$(this).click(function(){
	  		var stepSize = 240;
		  	var totalStep = 2;
		  	if(timelineID=='1'){
		  		totalStep = 3;
		  	}
		  	var Timeline = $('#timeline-' + timelineID);
		  	// console.log(Timeline);
		  	var currentPos = Timeline.attr('rel');
		  	console.log(currentPos);
		  	if ( currentPos < totalStep ) {
			  	var targetPos = parseInt(currentPos) + 1;
			  	console.log('goto pos ' + targetPos);
			  	Timeline.attr('rel', targetPos);
			  	Timeline.css('transform','translate3d(-'+ stepSize * targetPos * 4 +'px,0,0)');
			  }
			  else {
			  	Timeline.attr('rel','0');
			  	Timeline.css('transform','');
			  }
	  	});
  	});
  	var timelineNode = $(this).find('li');
  	// console.log(timeline);
  	var timelineLine = $(this).find('ul');
  	timelineLine.each(function(index){
  		$(this).css('width',240 * timelineNode.length + 'px');
  		console.log(240 * timelineNode.length + 'px');
  	});
  	timelineNode.each(function(index){
  		var nodeId = index + 1;
  		// console.log('timeline-' + timelineID + '-' + nodeId);
  		var topPosition = getRandomIntInclusive(20,100);
  		if ( timelineID == 1 && nodeId == 12 ) {
  			topPosition = 30;
  		} else if ( timelineID == 2 && nodeId == 1 ) {
  			topPosition = 20;
  		}
  		var size = '';
  		if ( timelineID == 1 && nodeId == 12 ) { size = 'width: 110px; ';}
  		var caption = $(this).children('p')[0].innerHTML;
  		// $(this).append('<div class="event-thumb" style="top:' + topPosition + 'px"><a href="javascript:;" onclick="showPhoto(\'' + timelineID + '-' + nodeId + '\')"><img src="assets/images/events/thumb/' + timelineID + '-' + nodeId + '.jpg" alt=""></a></div>');
  		$(this).append('<div class="event-thumb" style="' + size + 'top:' + topPosition + 'px"><a href="assets/images/events/original/' + timelineID + '-' + nodeId + '.jpg" data-lightbox="event-' + timelineID + '" data-title="'+caption+'"><img src="assets/images/events/thumb/' + timelineID + '-' + nodeId + '.jpg" alt=""></a></div>');
  	});
  }); 
});

function showPhoto(id) {
	console.log(id);
	var lightbox = $('<div id="lightbox" flex="main:center cross:center"><img src="assets/images/events/original/' + id + '.jpg"></div>');
	lightbox.appendTo($('body'));
}