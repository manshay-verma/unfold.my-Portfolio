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

  /* ── About ────────────────────────────────────────────────────── */

  function renderAbout(about) {
    if (!about || (!about.title && !about.description)) return;

    var titleEl = qs('#about-section .heading-h3 .gsap-reveal, #about-section h3 .gsap-reveal');
    if (titleEl && about.title) titleEl.textContent = about.title;

    var descEls = qsa('#about-section .col-lg-4 p.gsap-reveal');
    if (descEls.length > 0 && about.description) {
      descEls[0].textContent = about.description;
    }

    // CV / resume link inside about
    var cvBtn = qs('#about-section a.btn-outline-pill');
    if (cvBtn) {
      // Will be overridden once resume data arrives, but point to api for now
      cvBtn.href = '/api/resume/';
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

      return '<div class="timeline__block gsap-reveal">' +
        '<div class="timeline__bullet"></div>' +
        '<div class="timeline__header">' +
        '<h4 class="timeline__title">' + (exp.company || '') + '</h4>' +
        '<h5 class="timeline__meta">' + (exp.position || '') + '</h5>' +
        '<p class="timeline__timeframe">' + timeRange + '</p>' +
        '</div>' +
        '<div class="timeline__desc"><p>' + (exp.description || '') + '</p></div>' +
        '</div>';
    }).join('');
  }

  /* ── Education Timeline ────────────────────────────────────────── */

  function renderEducation(education) {
    var container = qs('.about-timelines .col-lg-6:last-child .timeline');
    if (!container || !education || !education.length) return;
    container.innerHTML = education.map(function (edu) {
      var start = formatDateString(edu.start_year);
      var end = formatDateString(edu.end_year) || 'Present';
      var timeRange = start ? (start + ' – ' + end) : end;

      return '<div class="timeline__block gsap-reveal">' +
        '<div class="timeline__bullet"></div>' +
        '<div class="timeline__header">' +
        '<h4 class="timeline__title">' + (edu.institute || '') + '</h4>' +
        '<h5 class="timeline__meta">' + (edu.degree || '') + '</h5>' +
        '<p class="timeline__timeframe">' + timeRange + '</p>' +
        '</div>' +
        '<div class="timeline__desc"><p>' + (edu.description || '') + '</p></div>' +
        '</div>';
    }).join('');
  }

  /* ── Skills ────────────────────────────────────────────────────── */

  function renderSkills(skills) {
    var container = qs('#skills-section .row.gutter-v3') || qs('#skills-section .row.gutter-v4');
    if (!container || !skills.length) return;

    container.innerHTML = skills.map(function (s) {
      var icon = s.icon || 'fa-solid fa-code';
      var desc = s.description || '';
      var categoryBadge = s.category ? '<span style="position: absolute; top: 18px; right: 18px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; color: #a78bfa; background: rgba(167, 139, 250, 0.12); border: 1px solid rgba(167, 139, 250, 0.25); padding: 3px 10px; border-radius: 20px;">' + s.category + '</span>' : '';

      return '<div class="col-md-6 col-lg-4 mb-4">' +
        '<div class="feature-v1" style="position: relative; height: 100%; display: flex; flex-direction: column; background: #13161e; border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 24px; transition: transform 0.3s ease, border-color 0.3s ease;">' +
        categoryBadge +
        '<div class="wrap-icon mb-3">' +
        '<i class="' + icon + '" style="font-size: 32px; color: #818cf8;"></i>' +
        '</div>' +
        '<h3 style="font-size: 17px; font-weight: 600; color: #f8fafc; margin-bottom: 10px;">' + s.name + '</h3>' +
        '<p style="font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 20px; flex: 1;">' + desc + '</p>' +
        '<div class="skill-percentage-bar" style="margin-top: auto; height: 6px; background: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden;">' +
        '<div class="skill-percentage-fill" style="width: ' + s.percentage + '%; height: 100%; background: linear-gradient(90deg, #7c6af5, #a78bfa); border-radius: 10px;"></div>' +
        '</div>' +
        '</div></div>';
    }).join('');
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
      
        var fallbackHtml = '<div style="width:100%; aspect-ratio: 4/3; background:#222; display:flex; align-items:center; justify-content:center;"><i class="icon-image" style="font-size:40px;color:#555;"></i></div>';
        
        return '<div class="item ' + cls + ' col-sm-6 col-md-6 col-lg-4 isotope-mb-2">' +
          '<a href="' + href + '" class="portfolio-item' + portrait + ' isotope-item gsap-reveal-img" data-slug="' + proj.slug + '">' +
          '<div class="overlay">' +
          '<span class="wrap-icon icon-link2"></span>' +
          '<div class="portfolio-item-content">' +
          '<h3>' + proj.title + '</h3>' +
          '<p>' + (proj.short_description || '') + '</p>' +
          '</div></div>' +
          (imgSrc ? '<img src="' + imgSrc + '" class="lazyload img-fluid" alt="' + proj.title + '">' : fallbackHtml) +
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
    if (typeof jQuery !== 'undefined' && jQuery('#posts').data('isotope')) {
      jQuery('#posts').isotope('reloadItems').isotope();
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
      return '<div class="col-md-6 col-lg-4 mb-4">' +
        '<div class="feature-v1">' +
        '<div class="wrap-icon mb-3">' +
        (c.certificate_image ? '<img src="' + absUrl(c.certificate_image) + '" style="height:80px; object-fit:contain; margin-bottom:10px;" alt="' + c.title + '">' : '<i class="icon-file-text-o"></i>') +
        '</div>' +
        '<h3>' + c.title + '</h3>' +
        '<p>' + c.issuer + ' &bull; ' + c.issue_date + '</p>' +
        (c.certificate_url ? '<p><a href="' + c.certificate_url + '" target="_blank" class="readmore">View Credential</a></p>' : '') +
        '</div></div>';
    }).join('');
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

      return '<div class="col-sm-6 col-md-6 col-lg-4 mb-4" data-aos="fade-up">' +
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
  }

  window.openJournalModal = function(index) {
    if (!window.journalData || !window.journalData[index]) return;
    var j = window.journalData[index];
    
    var readTime = j.read_time ? (j.read_time.toLowerCase().includes('min') ? j.read_time : j.read_time + ' mins read') : '3 mins read';
    var pubDate = j.publish_date || (j.created_at ? j.created_at.split('T')[0] : '');

    var titleEl = el('journalModalTitle');
    if (titleEl) titleEl.innerText = j.title;
    
    var metaEl = el('journalModalMeta');
    if (metaEl) metaEl.innerHTML = 'By ' + (j.author || 'Admin') + (pubDate ? ' &bull; ' + pubDate : '') + ' &bull; ' + readTime;
    
    var excerptEl = el('journalModalExcerpt');
    if (excerptEl) excerptEl.innerText = j.excerpt || '';
    
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
    if (!modalLinksEl) {
      modalLinksEl = document.createElement('div');
      modalLinksEl.id = 'journalModalLinks';
      modalLinksEl.style.cssText = 'margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 8px;';
      var parentBody = el('journalModalExcerpt') ? el('journalModalExcerpt').parentNode : null;
      var readMoreBtn = el('journalModalReadMoreBtn');
      if (parentBody && readMoreBtn) {
        parentBody.insertBefore(modalLinksEl, readMoreBtn);
      }
    }
    if (j.external_urls && Array.isArray(j.external_urls) && j.external_urls.length > 0) {
      modalLinksEl.style.display = 'flex';
      modalLinksEl.innerHTML = j.external_urls.map(function(link) {
        return '<a href="' + link.url + '" target="_blank" class="btn btn-sm" style="background: rgba(124, 106, 245, 0.2); color: #a78bfa; border: 1px solid rgba(124, 106, 245, 0.4); border-radius: 20px; font-size: 12px; font-weight: 500; padding: 6px 14px; text-decoration: none;"><i class="fa-solid fa-arrow-up-right-from-square"></i> ' + (link.title || 'Link') + '</a>';
      }).join('');
    } else if (modalLinksEl) {
      modalLinksEl.style.display = 'none';
    }
    
    var readMoreBtn = el('journalModalReadMoreBtn');
    if (readMoreBtn) readMoreBtn.href = '/journal/' + j.slug + '/';
    
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
