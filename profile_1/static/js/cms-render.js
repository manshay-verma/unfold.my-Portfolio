/**
 * cms-render.js
 * Fetches /api/portfolio/ and populates every section of the page dynamically.
 * Called once on DOMContentLoaded.
 */

(function () {
  'use strict';

  /* ── Helpers ──────────────────────────────────────────────────── */

  function el(id) { return document.getElementById(id); }
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return (root || document).querySelectorAll(sel); }
  function absUrl(path) {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    return window.location.origin + path;
  }

  /* ── Hero ─────────────────────────────────────────────────────── */

  function renderHero(hero) {
    // Don't overwrite if singleton has no meaningful data yet
    if (!hero || (!hero.name && !hero.headline && !hero.background_image)) return;

    // Background image via jarallax
    var heroSection = qs('#home-section');
    if (heroSection && hero.background_image) {
      heroSection.style.backgroundImage = "url('" + absUrl(hero.background_image) + "')";
    }

    // Subheading
    var subheading = qs('.hero-subheading');
    if (subheading && hero.headline) subheading.textContent = hero.headline;

    // Hero title animation markup — inject name letters
    var heroTitle = el('hero-title');
    if (heroTitle && hero.name) {
      var name = hero.name.trim();
      // First letter drives the animation (M -> rest)
      var firstLetter = name.charAt(0);
      var restLetters = name.slice(1).split('');

      // Rebuild intro-wrapper first letter
      var letterM = qs('.letter-m', heroTitle);
      if (letterM) letterM.textContent = firstLetter;

      // Rebuild final-wrapper letters
      var mTarget = qs('.m-target', heroTitle);
      if (mTarget) mTarget.textContent = firstLetter;

      var manshayPart = qs('.manshay-part', heroTitle);
      if (manshayPart) {
        manshayPart.innerHTML = restLetters.map(function (c) {
          return '<span class="letter anshay-letter">' + c + '</span>';
        }).join('');
      }
    }

    // Resume button
    if (hero.resume) {
      var resumeBtn = qs('.btn-download-cv, a[href="#resume"]');
      if (resumeBtn) {
        resumeBtn.href = absUrl(hero.resume);
        resumeBtn.target = '_blank';
      }
    }

    // Now fire the animation after DOM is updated
    if (typeof initHeroAnimation === 'function') {
      setTimeout(initHeroAnimation, 200);
    }
  }

  function triggerGsapReveal(container) {
    if (typeof jQuery === 'undefined' || !container) return;
    var $ = jQuery;
    var $reveals = $(container).find('.gsap-reveal');
    $reveals.each(function() {
      if (!$(this).find('.cover').length) {
        $(this).append('<span class="cover"></span>');
      }
    });

    if (typeof ScrollMagic !== 'undefined' && typeof TimelineMax !== 'undefined') {
      try {
        var controller = window.controller || new ScrollMagic.Controller();
        $reveals.each(function() {
          if ($(this).data('gsap-bound')) return;
          $(this).data('gsap-bound', true);
          var cover = $(this).find('.cover');
          var tl = new TimelineMax();
          tl.fromTo(cover, 1.5, { skewX: 0 }, { xPercent: 101, transformOrigin: "0% 100%", ease: Expo.easeInOut });
          new ScrollMagic.Scene({
            triggerElement: this,
            triggerHook: 0.85,
            reverse: false
          })
          .setTween(tl)
          .addTo(controller);
        });
      } catch (err) {
        console.log("GSAP trigger error:", err);
      }
    }
  }

  /* ── About ────────────────────────────────────────────────────── */

  function renderAbout(about) {
    if (!about || (!about.title && !about.description)) return;

    var titleWrap = el('about-title-wrap');
    if (titleWrap && about.title) {
      titleWrap.style.fontSize = '28px';
      titleWrap.style.fontWeight = '700';
      titleWrap.style.lineHeight = '1.4';
      titleWrap.style.color = '#ffffff';
      titleWrap.style.marginBottom = '24px';
      titleWrap.innerHTML = '<span class="gsap-reveal">' + about.title + '</span>';
      triggerGsapReveal(titleWrap);
    }

    var descWrap = el('about-description-wrap');
    if (descWrap && about.description) {
      var rawParagraphs = about.description.split(/\r?\n+/);
      var validParagraphs = [];
      for (var i = 0; i < rawParagraphs.length; i++) {
        var trimmed = rawParagraphs[i].trim();
        if (trimmed) validParagraphs.push(trimmed);
      }
      if (validParagraphs.length > 0) {
        descWrap.innerHTML = validParagraphs.map(function (pText, idx) {
          return '<p class="mb-4 gsap-reveal" style="font-size: 18px; line-height: 32px; color: rgba(255, 255, 255, 0.85); font-weight: 400; margin-bottom: 24px;">' + pText + '</p>';
        }).join('');
        triggerGsapReveal(descWrap);
      }
    }

    // About image
    var aboutImg = qs('#about-section .dotted-bg img');
    if (aboutImg && about.profile_image) {
      aboutImg.src = absUrl(about.profile_image);
      aboutImg.alt = about.title || 'About';
    }
  }

  function formatDateString(str) {
    if (!str) return '';
    var s = String(str).trim();
    if (s.toLowerCase() === 'present' || s.toLowerCase() === 'current') return 'Present';

    var parts = s.split('-');
    if (parts.length >= 2) {
      var year = parts[0];
      var monthIdx = parseInt(parts[1], 10) - 1;
      var months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];
      if (monthIdx >= 0 && monthIdx < 12 && year.length === 4) {
        return months[monthIdx] + ' ' + year;
      }
    }
    return s;
  }

  /* ── Experience Timeline ───────────────────────────────────────── */

  function renderExperience(experience) {
    var container = qs('.about-timelines .col-lg-6:first-child .timeline');
    if (!container || !experience || !experience.length) return;
    container.innerHTML = experience.map(function (exp) {
      var start = formatDateString(exp.start_date);
      var end = formatDateString(exp.end_date) || 'Present';
      var timeRange = start ? (start + ' – ' + end) : end;

      var techHtml = '';
      if (exp.technologies && Array.isArray(exp.technologies) && exp.technologies.length) {
        techHtml = '<div class="timeline__techs mt-3" style="display: flex; flex-wrap: wrap; gap: 6px;">' +
          exp.technologies.map(function (t) {
            return '<span class="tech-badge" style="background: rgba(167, 139, 250, 0.12); color: #a78bfa; border: 1px solid rgba(167, 139, 250, 0.25); font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 500; letter-spacing: 0.3px;">' + t + '</span>';
          }).join('') +
          '</div>';
      }

      return '<div class="timeline__block gsap-reveal">' +
        '<div class="timeline__bullet"></div>' +
        '<div class="timeline__header">' +
        '<h4 class="timeline__title">' + (exp.company || '') + '</h4>' +
        '<h5 class="timeline__meta">' + (exp.position || '') + '</h5>' +
        '<p class="timeline__timeframe">' + timeRange + '</p>' +
        '</div>' +
        '<div class="timeline__desc"><p>' + (exp.description || '') + '</p>' + techHtml + '</div>' +
        '</div>';
    }).join('');
    triggerGsapReveal(container);
  }

  /* ── Education Timeline ────────────────────────────────────────── */

  function renderEducation(education) {
    var container = qs('.about-timelines .col-lg-6:last-child .timeline');
    if (!container || !education || !education.length) return;
    container.innerHTML = education.map(function (edu) {
      var start = formatDateString(edu.start_year);
      var end = formatDateString(edu.end_year) || 'Present';
      var timeRange = start ? (start + ' – ' + end) : end;

      var specHtml = '';
      if (edu.specializations && Array.isArray(edu.specializations) && edu.specializations.length) {
        specHtml = '<div class="timeline__specs mt-3" style="display: flex; flex-wrap: wrap; gap: 6px;">' +
          edu.specializations.map(function (s) {
            return '<span class="spec-badge" style="background: rgba(59, 130, 246, 0.12); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.25); font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 500; letter-spacing: 0.3px;">' + s + '</span>';
          }).join('') +
          '</div>';
      }

      return '<div class="timeline__block gsap-reveal">' +
        '<div class="timeline__bullet"></div>' +
        '<div class="timeline__header">' +
        '<h4 class="timeline__title">' + (edu.institute || '') + '</h4>' +
        '<h5 class="timeline__meta">' + (edu.degree || '') + '</h5>' +
        '<p class="timeline__timeframe">' + timeRange + '</p>' +
        '</div>' +
        '<div class="timeline__desc"><p>' + (edu.description || '') + '</p>' + specHtml + '</div>' +
        '</div>';
    }).join('');
    triggerGsapReveal(container);
  }

  /* ── Skills ────────────────────────────────────────────────────── */

  function renderSkills(skills) {
    var container = qs('#skills-section .row.gutter-v3') || qs('#skills-section .row.gutter-v4');
    if (!container || !skills.length) return;

    container.innerHTML = skills.map(function (s) {
      var icon = s.icon || 'fa-solid fa-code';
      var desc = s.description || '';
      var categoryBadge = s.category ? '<span style="display: inline-block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; color: #a78bfa; background: rgba(167, 139, 250, 0.12); border: 1px solid rgba(167, 139, 250, 0.25); padding: 4px 12px; border-radius: 20px;">' + s.category + '</span>' : '';

      return '<div class="col-md-6 col-lg-4 mb-4 gsap-reveal">' +
        '<div class="feature-v1" style="height: 100%; display: flex; flex-direction: column; background: #13161e; border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 24px; transition: transform 0.3s ease, border-color 0.3s ease;">' +
        '<div style="display: flex; align-items: center; justify-content: space-between; width: 100%; margin-bottom: 16px;">' +
        '<div class="wrap-icon" style="margin-bottom: 0;">' +
        '<i class="' + icon + '" style="font-size: 30px; color: #818cf8;"></i>' +
        '</div>' +
        categoryBadge +
        '</div>' +
        '<h3 style="font-size: 17px; font-weight: 600; color: #f8fafc; margin-bottom: 10px;">' + s.name + '</h3>' +
        '<p style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 20px; flex: 1;">' + desc + '</p>' +
        '<div class="skill-percentage-bar" style="margin-top: auto; height: 6px; background: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden;">' +
        '<div class="skill-percentage-fill" style="width: ' + s.percentage + '%; height: 100%; background: linear-gradient(90deg, #7c6af5, #a78bfa); border-radius: 10px; transition: width 1.2s ease;"></div>' +
        '</div>' +
        '</div></div>';
    }).join('');

    triggerGsapReveal(container);
  }

  function renderProjects(projects) {
    var container = el('posts');
    if (!container) return;
    if (!projects || !projects.length) {
      container.innerHTML = '<div class="col-12 text-center mt-5"><p>No projects yet.</p></div>';
      return;
    }

    var classes = ['web branding', 'branding packaging', 'web packaging',
      'illustration packaging', 'web branding', 'branding packaging'];

    container.innerHTML = projects.map(function (proj, idx) {
      var cls = classes[idx % classes.length];
      var imgSrc = proj.cover_image ? absUrl(proj.cover_image) : '';
      var href = '/portfolio-single/' + proj.slug + '/';
      var portrait = idx % 3 === 1 ? ' item-portrait' : '';
      
        var fallbackHtml = '<div style="width:100%; aspect-ratio: 4/3; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-code" style="font-size:38px; color:rgba(255,255,255,0.35);"></i></div>';
        
        var techText = proj.short_description || (Array.isArray(proj.tech_stack) ? proj.tech_stack.join(', ') : '');

        return '<div class="item ' + cls + ' col-sm-6 col-md-6 col-lg-4 isotope-mb-2">' +
          '<a href="' + href + '" class="portfolio-item' + portrait + ' isotope-item gsap-reveal-img" data-slug="' + proj.slug + '" style="border-radius: 14px; overflow: hidden; display: block; position: relative;">' +
          '<div class="overlay" style="display:flex; flex-direction:column; justify-content:space-between; padding:22px; background: linear-gradient(to top, rgba(15, 17, 26, 0.95) 0%, rgba(15, 17, 26, 0.4) 60%, rgba(15, 17, 26, 0.2) 100%); transition: all 0.3s ease;">' +
          '<div style="display:flex; justify-content:flex-end;"><span class="wrap-icon" style="font-size:14px; color:#a78bfa; background:rgba(167, 139, 250, 0.2); border: 1px solid rgba(167, 139, 250, 0.3); width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-arrow-up-right-from-square"></i></span></div>' +
          '<div class="portfolio-item-content" style="position:relative; bottom:auto; left:auto; right:auto; padding:0; margin:0; width:100%;">' +
          '<h3 style="font-size:16px; font-weight:700; color:#f8fafc; margin:0 0 6px 0; line-height:1.35; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">' + proj.title + '</h3>' +
          '<p style="font-size:12px; font-weight:600; color:#a78bfa; margin:0; line-height:1.4; text-transform:uppercase; letter-spacing:0.5px; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden;">' + techText + '</p>' +
          '</div></div>' +
          (imgSrc ? '<img src="' + imgSrc + '" class="lazyload img-fluid" alt="' + proj.title + '" style="width:100%; height:100%; object-fit:cover;">' : fallbackHtml) +
          '</a></div>';
    }).join('');

    // Event delegation for dynamically added project cards
    document.querySelector('#posts').addEventListener('click', function(e) {
      var card = e.target.closest('.portfolio-item');
      if (card && card.dataset.slug) {
        e.preventDefault();
        window.location.href = '/portfolio-single/' + card.dataset.slug + '/';
      }
    });

    // Re-initialise isotope if already loaded
    if (typeof jQuery !== 'undefined') {
      var $ = jQuery;
      if ($('#posts').data('isotope')) {
        $('#posts').isotope('reloadItems').isotope();
      }
      $('#posts .gsap-reveal-img').each(function() {
        if (!$(this).find('.reveal-wrap').length) {
          var html = $(this).html();
          $(this).html('<div class="reveal-wrap"><span class="cover"></span><div class="reveal-content">'+html+'</div></div>');
        }
      });
      if (typeof ScrollMagic !== 'undefined' && typeof TimelineMax !== 'undefined') {
        try {
          var controller = window.controller || new ScrollMagic.Controller();
          $('#posts .gsap-reveal-img').each(function() {
            var cover = $(this).find('.cover'),
                revealContent = $(this).find('.reveal-content'),
                img = $(this).find('.reveal-content img');
            if (cover.length && !$(this).data('gsap-bound')) {
              $(this).data('gsap-bound', true);
              var tl2 = new TimelineMax();
              tl2.set(img, { scale: '2.0', autoAlpha: 1 })
                 .to(cover, 0.8, { marginLeft: '0', ease: Expo.easeInOut })
                 .set(revealContent, { autoAlpha: 1 })
                 .to(cover, 0.8, { marginLeft: '102%', ease: Expo.easeInOut })
                 .to(img, 1.5, { scale: '1.0', ease: Expo.easeOut }, '-=1.2');

              new ScrollMagic.Scene({
                triggerElement: this,
                triggerHook: 0.85,
                reverse: false
              })
              .setTween(tl2)
              .addTo(controller);
            }
          });
        } catch (err) {
          console.log("Project GSAP error:", err);
        }
      }
    }
  }

  /* ── Contact ────────────────────────────────────────────────────── */

  function renderContact(contact) {
    if (!contact || (!contact.email && !contact.phone && !contact.address)) return;
    var emailEl = qs('#contact-section .contact-info-val[href^="mailto"]');
    if (emailEl && contact.email) {
      emailEl.href = 'mailto:' + contact.email;
      emailEl.textContent = contact.email;
    }
    var phoneEl = qs('#contact-section .contact-info-val[href="#"]');
    if (phoneEl && contact.phone) {
      phoneEl.href = 'tel:' + contact.phone;
      phoneEl.textContent = contact.phone;
    }
    var addressEl = qs('#contact-section address.contact-info-val');
    if (addressEl && contact.address) addressEl.innerHTML = contact.address;
  }

  /* ── Social Links ───────────────────────────────────────────────── */

  function renderSocial(social) {
    var footerUl = qs('.footer-site-social');
    if (!footerUl || !social || !social.length) return;
    footerUl.innerHTML = social.map(function (s) {
      return '<li><a href="' + s.url + '" target="_blank" rel="noopener">' + s.platform + '</a></li>';
    }).join('');
  }

  /* ── Resume ─────────────────────────────────────────────────────── */

  function renderResume(resume) {
    if (!resume || !resume.pdf) return;
    var pdfUrl = absUrl(resume.pdf);
    // Update any "Download CV" buttons
    qsa('a.btn-download-cv, a[href="/api/resume/"]').forEach(function (btn) {
      btn.href = pdfUrl;
      btn.target = '_blank';
    });
    // About section download button
    var aboutBtn = qs('#about-section a.btn-outline-pill');
    if (aboutBtn) {
      aboutBtn.href = pdfUrl;
      aboutBtn.target = '_blank';
      aboutBtn.textContent = 'Download my CV';
    }
  }

  /* ── SEO ─────────────────────────────────────────────────────────── */

  function renderSEO(seo) {
    if (!seo) return;
    if (seo.site_title) document.title = seo.site_title;
    var metaDesc = qs('meta[name="description"]');
    if (metaDesc && seo.meta_description) metaDesc.setAttribute('content', seo.meta_description);
    var metaKw = qs('meta[name="keywords"]');
    if (metaKw && seo.keywords) metaKw.setAttribute('content', seo.keywords);
    if (seo.favicon) {
      var link = qs('link[rel="icon"], link[rel="shortcut icon"]');
      if (!link) { link = document.createElement('link'); link.rel = 'icon'; document.head.appendChild(link); }
      link.href = absUrl(seo.favicon);
    }
  }

  /* ── Certifications ──────────────────────────────────────────────── */

  function renderCertifications(certs) {
    // If a certifications container exists, populate it
    var container = el('certifications-section') || qs('.certifications-row');
    if (!container || !certs.length) return;
    container.innerHTML = certs.map(function (c) {
      return '<div class="col-md-6 col-lg-4 mb-4 gsap-reveal">' +
        '<div class="feature-v1">' +
        '<div class="wrap-icon mb-3">' +
        (c.certificate_image ? '<img src="' + absUrl(c.certificate_image) + '" style="height:80px; object-fit:contain; margin-bottom:10px;" alt="' + c.title + '">' : '<i class="icon-file-text-o"></i>') +
        '</div>' +
        '<h3>' + c.title + '</h3>' +
        '<p>' + c.issuer + ' &bull; ' + c.issue_date + '</p>' +
        (c.certificate_url ? '<p><a href="' + c.certificate_url + '" target="_blank" class="readmore">View Credential</a></p>' : '') +
        '</div></div>';
    }).join('');

    triggerGsapReveal(container);
  }

  /* ── Journal ──────────────────────────────────────────────────── */

  function renderJournal(journals) {
    var container = el('journal-row');
    if (!container || !journals.length) return;

    window.journalData = journals;

    container.innerHTML = journals.map(function (j, index) {
      var img = j.image ? absUrl(j.image) : '';
      var readTime = j.read_time ? (j.read_time.toLowerCase().includes('min') ? j.read_time : j.read_time + ' mins read') : '3 mins read';
      var pubDate = j.publish_date || (j.created_at ? j.created_at.split('T')[0] : '');

      var mediaHtml = img
        ? '<div style="height: 190px; overflow: hidden; position: relative;"><img src="' + img + '" alt="' + j.title + '" style="width:100%; height:100%; object-fit:cover; transition: transform 0.4s ease;" class="journal-card-img" /></div>'
        : '<div style="height: 150px; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-book-open" style="font-size:38px; color:rgba(255,255,255,0.35);"></i></div>';

      var linksHtml = '';
      if (j.external_urls && Array.isArray(j.external_urls) && j.external_urls.length > 0) {
        linksHtml = '<div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">' +
          j.external_urls.map(function(link) {
            return '<a href="' + link.url + '" target="_blank" onclick="event.stopPropagation();" style="font-size: 11px; padding: 3px 10px; border-radius: 12px; background: rgba(167, 139, 250, 0.15); color: #c4b5fd; text-decoration: none; border: 1px solid rgba(167, 139, 250, 0.3); display: inline-flex; align-items: center; gap: 4px;"><i class="fa-solid fa-link" style="font-size:9px;"></i> ' + (link.title || 'Link') + '</a>';
          }).join('') +
          '</div>';
      }

      return '<div class="col-sm-6 col-md-6 col-lg-4 mb-4" data-aos="fade-up" data-aos-delay="' + (index * 100) + '">' +
        '<div onclick="openJournalModal(' + index + ')" class="journal-card" style="background:#13161e; border:1px solid rgba(255,255,255,0.08); border-radius:14px; overflow:hidden; height:100%; cursor:pointer; display:flex; flex-direction:column; transition: all 0.3s ease; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">' +
        mediaHtml +
        '<div style="padding: 20px; flex: 1; display: flex; flex-direction: column;">' +
        '<div style="font-size:11.5px; font-weight:600; color:#a78bfa; text-transform:uppercase; letter-spacing:0.8px; margin-bottom: 8px;">' +
        'By ' + (j.author || 'Admin') + (pubDate ? ' &bull; ' + pubDate : '') + ' &bull; ' + readTime +
        '</div>' +
        '<h3 style="font-size:17px; font-weight:600; color:#f8fafc; margin:0 0 10px; line-height:1.4;">' + j.title + '</h3>' +
        '<p style="font-size:13.5px; color:#94a3b8; line-height:1.6; margin-bottom:14px; flex:1; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden;">' + (j.excerpt || '') + '</p>' +
        linksHtml +
        '<div style="display:flex; align-items:center; gap:8px; font-size:13px; font-weight:600; color:#818cf8; margin-top:14px;">' +
        '<span>Quick Preview</span> <i class="fa-solid fa-arrow-right" style="font-size:11px;"></i>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>';
    }).join('');

    if (typeof AOS !== 'undefined') {
      AOS.refresh();
    }
  }

  window.closeJournalModal = function() {
    if (typeof $ !== 'undefined' && $('#journalModal').length && typeof $('#journalModal').modal === 'function') {
      $('#journalModal').modal('hide');
    }
    var m = el('journalModal');
    if (m) {
      m.classList.remove('show');
      m.style.display = 'none';
      document.body.classList.remove('modal-open');
      var backdrop = document.querySelector('.modal-backdrop');
      if (backdrop && backdrop.parentNode) {
        backdrop.parentNode.removeChild(backdrop);
      }
    }
  };

  window.openJournalModal = function(index) {
    if (!window.journalData || !window.journalData[index]) return;
    var j = window.journalData[index];
    
    var readTime = j.read_time ? (j.read_time.toLowerCase().includes('min') ? j.read_time : j.read_time + ' mins read') : '3 mins read';
    var pubDate = formatDateString(j.publish_date) || (j.created_at ? j.created_at.split('T')[0] : '');

    var titleEl = el('journalModalTitle');
    if (titleEl) titleEl.innerText = j.title || 'Journal Preview';
    
    var metaEl = el('journalModalMeta');
    if (metaEl) {
      metaEl.innerHTML = '<span style="display: inline-flex; align-items: center; gap: 6px;"><i class="fa-solid fa-user-pen" style="color:#818cf8;"></i> By ' + (j.author || 'Admin') + '</span>' +
        (pubDate ? ' <span style="margin:0 8px; color:rgba(255,255,255,0.2);">|</span> <span style="display: inline-flex; align-items: center; gap: 6px;"><i class="fa-solid fa-calendar-days" style="color:#818cf8;"></i> ' + pubDate + '</span>' : '') +
        ' <span style="margin:0 8px; color:rgba(255,255,255,0.2);">|</span> <span style="display: inline-flex; align-items: center; gap: 6px;"><i class="fa-solid fa-clock" style="color:#818cf8;"></i> ' + readTime + '</span>';
    }
    
    var excerptEl = el('journalModalExcerpt');
    if (excerptEl) excerptEl.innerText = j.excerpt || (j.content ? j.content.replace(/<[^>]+>/g, '').substring(0, 200) + '...' : '');
    
    var imgContainer = el('journalModalImageContainer');
    if (imgContainer) {
      if (j.image) {
        imgContainer.style.display = 'block';
        imgContainer.style.backgroundImage = 'url(' + absUrl(j.image) + ')';
      } else {
        imgContainer.style.display = 'none';
      }
    }

    var modalLinksEl = el('journalModalLinks');
    if (modalLinksEl) {
      if (j.external_urls && Array.isArray(j.external_urls) && j.external_urls.length > 0) {
        modalLinksEl.style.display = 'flex';
        modalLinksEl.innerHTML = j.external_urls.map(function(link) {
          return '<a href="' + link.url + '" target="_blank" style="background: rgba(167, 139, 250, 0.12); color: #a78bfa; border: 1px solid rgba(167, 139, 250, 0.25); border-radius: 20px; font-size: 12px; font-weight: 600; padding: 6px 14px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;"><i class="fa-solid fa-arrow-up-right-from-square"></i> ' + (link.title || 'Link') + '</a>';
        }).join('');
      } else {
        modalLinksEl.style.display = 'none';
      }
    }
    
    var readMoreBtn = el('journalModalReadMoreBtn');
    if (readMoreBtn) {
      var targetUrl = '/journal/' + (j.slug || '') + '/';
      readMoreBtn.href = targetUrl;
      readMoreBtn.onclick = function(e) {
        e.preventDefault();
        window.location.href = targetUrl;
      };
    }
    
    if (typeof $ !== 'undefined' && $('#journalModal').length && typeof $('#journalModal').modal === 'function') {
      $('#journalModal').modal('show');
    } else {
      var m = el('journalModal');
      if (m) {
        m.classList.add('show');
        m.style.display = 'block';
      }
    }
  };

  /* ── Bootstrap fetch ──────────────────────────────────────────────── */

  document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/portfolio/')
      .then(function (res) {
        if (!res.ok) throw new Error('API error: ' + res.status);
        return res.json();
      })
      .then(function (data) {
        renderSEO(data.seo);
        renderHero(data.hero);          // also fires initHeroAnimation()
        renderAbout(data.about);
        renderExperience(data.experience);
        renderEducation(data.education);
        renderSkills(data.skills);
        renderProjects(data.projects);
        renderCertifications(data.certifications);
        if (data.journals) renderJournal(data.journals);
        renderResume(data.resume);
        renderContact(data.contact);
        renderSocial(data.social);
        if (typeof AOS !== 'undefined') {
          AOS.refresh();
        }
      })
      .catch(function (err) {
        console.warn('[CMS] Failed to load portfolio data:', err.message);
        // Graceful degradation: existing static content remains visible
      });
  });

})();
