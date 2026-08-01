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

  /* ── Experience Timeline ───────────────────────────────────────── */

  function renderExperience(experience) {
    var container = qs('.about-timelines .col-lg-6:first-child .timeline');
    if (!container || !experience || !experience.length) return;
    container.innerHTML = experience.map(function (exp) {
      return '<div class="timeline__block gsap-reveal">' +
        '<div class="timeline__bullet"></div>' +
        '<div class="timeline__header">' +
        '<h4 class="timeline__title">' + (exp.company || '') + '</h4>' +
        '<h5 class="timeline__meta">' + (exp.position || '') + '</h5>' +
        '<p class="timeline__timeframe">' + (exp.start_date || '') + ' – ' + (exp.end_date || '') + '</p>' +
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
      return '<div class="timeline__block gsap-reveal">' +
        '<div class="timeline__bullet"></div>' +
        '<div class="timeline__header">' +
        '<h4 class="timeline__title">' + (edu.institute || '') + '</h4>' +
        '<h5 class="timeline__meta">' + (edu.degree || '') + '</h5>' +
        '<p class="timeline__timeframe">' + (edu.start_year || '') + ' – ' + (edu.end_year || '') + '</p>' +
        '</div>' +
        '<div class="timeline__desc"><p>' + (edu.description || '') + '</p></div>' +
        '</div>';
    }).join('');
  }

  /* ── Skills ────────────────────────────────────────────────────── */

  function renderSkills(skills) {
    var container = qs('#skills-section .row.gutter-v4');
    if (!container || !skills.length) return;
    // Group by category
    var groups = {};
    skills.forEach(function (s) {
      var cat = s.category || 'Other';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(s);
    });

    container.innerHTML = Object.keys(groups).map(function (cat) {
      var catSkills = groups[cat];
      var tags = catSkills.map(function (s) {
        return '<span class="tech-tag">' + s.name + '</span>';
      }).join('');
      var icon = catSkills[0].icon || 'icon-cogs';
      return '<div class="col-md-6 col-lg-4 mb-4 gsap-reveal">' +
        '<div class="skill-card">' +
        '<div class="icon-wrap"><span class="' + icon + '"></span></div>' +
        '<h3>' + cat + '</h3>' +
        '<div class="tech-tags">' + tags + '</div>' +
        '</div></div>';
    }).join('');
  }

  /* ── Projects ───────────────────────────────────────────────────── */

  function renderProjects(projects) {
    var container = el('posts');
    if (!container || !projects.length) return;

    var classes = ['web branding', 'branding packaging', 'web packaging',
      'illustration packaging', 'web branding', 'branding packaging'];

    container.innerHTML = projects.map(function (proj, idx) {
      var cls = classes[idx % classes.length];
      var imgSrc = proj.cover_image ? absUrl(proj.cover_image) : '';
      var href = '/portfolio-single/' + proj.slug + '/';
      var portrait = idx % 3 === 1 ? ' item-portrait' : '';
      return '<div class="item ' + cls + ' col-sm-6 col-md-6 col-lg-4 isotope-mb-2">' +
        '<a href="' + href + '" class="portfolio-item ajax-load-page' + portrait + ' isotope-item gsap-reveal-img" data-id="' + proj.id + '">' +
        '<div class="overlay">' +
        '<span class="wrap-icon icon-link2"></span>' +
        '<div class="portfolio-item-content">' +
        '<h3>' + proj.title + '</h3>' +
        '<p>' + (proj.short_description || '') + '</p>' +
        '</div></div>' +
        (imgSrc ? '<img src="' + imgSrc + '" class="lazyload img-fluid" alt="' + proj.title + '">' : '') +
        '</a></div>';
    }).join('');

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
      return '<div class="col-sm-6 col-md-4 col-lg-3 mb-4">' +
        '<div class="cert-card" style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:20px;text-align:center;">' +
        (c.certificate_image ? '<img src="' + absUrl(c.certificate_image) + '" style="max-height:80px;object-fit:contain;margin-bottom:12px;" alt="">' : '') +
        '<h5 style="font-size:14px;font-weight:600;margin-bottom:4px;">' + c.title + '</h5>' +
        '<p style="font-size:12px;color:#8892a4;margin:0;">' + c.issuer + ' · ' + c.issue_date + '</p>' +
        (c.certificate_url ? '<a href="' + c.certificate_url + '" target="_blank" style="font-size:11px;color:#a78bfa;display:block;margin-top:8px;">View Certificate →</a>' : '') +
        '</div></div>';
    }).join('');
  }

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
        renderResume(data.resume);
        renderContact(data.contact);
        renderSocial(data.social);
      })
      .catch(function (err) {
        console.warn('[CMS] Failed to load portfolio data:', err.message);
        // Graceful degradation: existing static content remains visible
      });
  });

})();
