(function($) {
  
  'use strict';
  
  // header plugin.
  $.fn.header = function() {
    return this.each(function() {
      var button = $('.js-header-button');
      var panel = $('.js-header-panel');
      var close = $('.js-header-close');
      var links = panel.find('a');
      
      // Attach click event listener.
      button.on('click', function(e) {
        panel.addClass('active');
        e.preventDefault();
      });
      close.on('click', function(e) {
        panel.removeClass('active');
        e.preventDefault();
      });
      links.on('click', function(e) {
        panel.removeClass('active');
      });
    });
  };
  
  // header2 plugin.
  $.fn.header2 = function() {
    return this.each(function() {
      var $this = $(this);
      var $window = $(window);
      function step(timestamp) {
        if ($window.scrollTop() > 0) {
          $this.addClass('active');
        } else {
          $this.removeClass('active');
        }
        window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    });
  };
  
  // backToTop plugin.
  $.fn.backToTop = function() {
    return this.each(function() {
      var $this = $(this);
      var $window = $(window);
      $this.hide();
      function step(timestamp) {
        if ($window.scrollTop() > 0) {
          $this.fadeIn();
        } else {
          $this.fadeOut();
        }
        window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    });
  };
  
  // reveal plugin
  $.fn.reveal = function() {
    return this.each(function() {
      var $this = $(this);
      var $window = $(window);
      function step(timestamp) {
        var margin = 24 - ($window.scrollTop() * 0.1);
        if (margin < 0) {
          margin = 0;
        }
        $this
          .css('margin-left', margin + 'px')
          .css('margin-right', margin + 'px')
          .css('margin-top', margin + 'px');
        window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    });
  };
  
  // tabs plugin.
  $.fn.tabs = function() {
    return this.each(function() {
      var $this = $(this);
      var headers = $this.find('.js-tabs-header');
      var panels = $this.find('.js-tabs-panel');
      panels.hide();
      headers.each(function(index, value) {
        var _this = $(value);
        var selector = _this.attr('href');
        var panel = $(selector);
        
        // Attach click event listener.
        _this.on('click', function(e) {
          headers.removeClass('active');
          _this.addClass('active');
          panels.hide();
          panel.fadeIn();
          e.preventDefault();
        });
      });
      headers.first().trigger('click');
    });
  };
  
  // more plugin.
  $.fn.more = function() {
    return this.each(function() {
      var $this = $(this);
      var length = $this.attr('data-more-length');
      var items = $this.find('.js-more-item');
      var navContainer = $this.find('.js-more-nav-container');
      var button = $this.find('.js-more-button');
      if (items.length > length) {
        items.slice(length).hide();
        navContainer.show();
        
        // Attach click event listener.
        button.on('click', function(e) {
          navContainer.hide();
          items.fadeIn();
          e.preventDefault();
        });
      }
    });
  };
  
  // detail plugin.
  $.fn.detail = function() {
    return this.each(function() {
      var $this = $(this);
      var items = $this.find('.js-detail-item');
      var headers = $this.find('.js-detail-header');
      var panel = $this.find('.js-detail-panel');
      var contents = $this.find('.js-detail-content');
      items.each(function() {
        var _this = $(this);
        var id = _this.attr('data-detail-id');
        var content = contents.filter('[data-detail-id="' + id + '"]');
        var header = _this.find('.js-detail-header');
        
        // Attach click event listener.
        header.on('click', function(e) {
          headers.removeClass('active');
          header.addClass('active');
          contents.hide();
          content.show();
          var position = _this.position();
          var item;
          items.each(function() {
            if (item == undefined) {
              var __this = $(this);
              var _position = __this.position();
              if (_position.top > position.top) {
                item = __this;
              }
            }
          });
          panel.insertBefore(item);
          panel.slideDown();
          //e.preventDefault();
        });
      });
    });
  };
  
   // collapse plugin.
  $.fn.collapse = function() {
    return this.each(function() {
      const $this = $(this);
      const header = $this.find('.js-collapse-header');
      
      // Attach click event listener.
      header.on('click', function(e) {
        $this.toggleClass('collapsed');
        e.preventDefault();
      });
    });
  };
  
  Drupal.behaviors.irc = {
    attach: function(context, settings) {
      if (context instanceof jQuery){
        context = context[0];
      }
      
      // Initialize header.
      $('.js-header', context).header();
      
      // Initialize header2.
      $('.js-header-2', context).header2();
      
      // Initialize backToTop.
      $('#back-to-top', context).backToTop();
      
      // Initialize reveal.
      $('.js-reveal', context).reveal();
      
      // Initialize tabs.
      $('.js-tabs', context).tabs();
      
      // Initialize owlCarousel.
      $('.js-carousel', context).owlCarousel({
        autoplay: true,
        autoplayTimeout: 7500,
        dots: false,
        items: 1,
        loop: true
      });
      
      // Initialize more.
      $('.js-more', context).more();
      
      // Initialize detail.
      $('.js-detail', context).detail();
      
      // Initialize collapse.
      $('.js-collapse').collapse();
    }
  };
})(jQuery36);