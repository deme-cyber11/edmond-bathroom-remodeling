/* ===== Mobile Nav Toggle ===== */
document.addEventListener('DOMContentLoaded',function(){
  var toggle=document.querySelector('.header__toggle');
  var nav=document.querySelector('.header__nav');
  if(toggle&&nav){
    toggle.addEventListener('click',function(){
      nav.classList.toggle('open');
      var expanded=nav.classList.contains('open');
      toggle.setAttribute('aria-expanded',expanded);
      toggle.innerHTML=expanded?'<i class="ph ph-x"></i>':'<i class="ph ph-list"></i>';
    });
    nav.querySelectorAll('a').forEach(function(link){
      link.addEventListener('click',function(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.innerHTML='<i class="ph ph-list"></i>';});
    });
  }

  /* ===== FAQ Accordion ===== */
  document.querySelectorAll('.faq-item__q').forEach(function(btn){
    btn.addEventListener('click',function(){
      var item=btn.closest('.faq-item');
      var wasActive=item.classList.contains('active');
      document.querySelectorAll('.faq-item').forEach(function(el){el.classList.remove('active');});
      if(!wasActive)item.classList.add('active');
    });
  });

  /* ===== Before/After Slider ===== */
  document.querySelectorAll('.ba-slider').forEach(function(slider){
    var afterImg=slider.querySelector('.ba-slider__after');
    var line=slider.querySelector('.ba-slider__line');
    var handle=slider.querySelector('.ba-slider__handle');
    var dragging=false;

    function move(x){
      var rect=slider.getBoundingClientRect();
      var pct=Math.max(0,Math.min(1,(x-rect.left)/rect.width))*100;
      afterImg.style.clipPath='inset(0 0 0 '+pct+'%)';
      line.style.left=pct+'%';
      handle.style.left=pct+'%';
    }

    slider.addEventListener('mousedown',function(e){dragging=true;move(e.clientX);});
    window.addEventListener('mousemove',function(e){if(dragging)move(e.clientX);});
    window.addEventListener('mouseup',function(){dragging=false;});
    slider.addEventListener('touchstart',function(e){dragging=true;move(e.touches[0].clientX);},{passive:true});
    window.addEventListener('touchmove',function(e){if(dragging)move(e.touches[0].clientX);},{passive:true});
    window.addEventListener('touchend',function(){dragging=false;});
  });

  /* ===== Sticky Header Shadow ===== */
  var header=document.querySelector('.header');
  if(header){
    window.addEventListener('scroll',function(){
      header.style.boxShadow=window.scrollY>10?'0 2px 20px rgba(0,0,0,.12)':'0 2px 12px rgba(0,0,0,.1)';
    },{passive:true});
  }
});
