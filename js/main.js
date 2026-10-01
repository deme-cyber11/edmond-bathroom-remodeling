/* ===== Mobile Nav Toggle ===== */
var ICON_X='<svg class="ic" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z"/></svg>';
var ICON_LIST='<svg class="ic" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M2 4.75A.75.75 0 0 1 2.75 4h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 4.75ZM2 10a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 10Zm0 5.25a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1-.75-.75Z" clip-rule="evenodd"/></svg>';
document.addEventListener('DOMContentLoaded',function(){
  var toggle=document.querySelector('.header__toggle');
  var nav=document.querySelector('.header__nav');
  if(toggle&&nav){
    toggle.addEventListener('click',function(){
      nav.classList.toggle('open');
      var expanded=nav.classList.contains('open');
      toggle.setAttribute('aria-expanded',expanded);
      toggle.innerHTML=expanded?ICON_X:ICON_LIST;
    });
    nav.querySelectorAll('a').forEach(function(link){
      link.addEventListener('click',function(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.innerHTML=ICON_LIST;});
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
