/**
 * Hero Section Cinematic Animation - Pixel Perfect Transition
 * Concept: Unfold.My -> Manshay using target positioning
 *
 * NOTE: initHeroAnimation() is exported so the API fetch in
 * cms-render.js can call it AFTER injecting hero data into the DOM.
 * The window.load listener is kept as a fallback for static HTML usage.
 */

window.addEventListener('load', function() {
    // Only fire automatically if hero-title already has data (static/fallback).
    // cms-render.js will call initHeroAnimation() after fetch completes.
    var title = document.getElementById('hero-title');
    if (title && title.querySelector('.letter-m')) {
        setTimeout(initHeroAnimation, 800);
    }
});

function initHeroAnimation() {
    const title = document.getElementById('hero-title');
    if (!title) return;

    const intro = title.querySelector('.intro-wrapper');
    const final = title.querySelector('.final-wrapper');
    if (!intro || !final) return;

    const mIntro = intro.querySelector('.letter-m');
    const mTarget = final.querySelector('.m-target');
    const anshay = final.querySelectorAll('.anshay-letter');
    const otherIntro = intro.querySelectorAll('.letter:not(.letter-m)');
    const subheading = document.querySelector('.hero-subheading');

    if (!mIntro || !mTarget) return;

    // Use TimelineMax for compatibility
    const tl = new TimelineMax();

    // 1. Calculate the exact pixel difference between intro M and final M
    const startRect = mIntro.getBoundingClientRect();
    const targetRect = mTarget.getBoundingClientRect();
    
    const deltaX = targetRect.left - startRect.left;
    const deltaY = targetRect.top - startRect.top;

    // 2. Setup initial states
    TweenMax.set(final, { opacity: 0, visibility: 'visible' });
    TweenMax.set(anshay, { opacity: 0, y: 15 });
    TweenMax.set(mTarget, { opacity: 0 }); // Hide target M initially
    if (subheading) TweenMax.set(subheading, { opacity: 0, y: 10 });

    tl
        // 1. Fade out other letters in "Unfold.My"
        .to(otherIntro, 0.6, { 
            opacity: 0, 
            y: -10,
            ease: Power2.easeOut 
        })

        // 2. Slide the M from its intro position to its final position
        .to(mIntro, 1.2, { 
            x: deltaX, 
            y: deltaY,
            ease: Expo.easeInOut 
        }, "-=0.3")

        // 3. Simultaneously reveal the final name wrapper and the anshay letters
        .to(final, 0.1, { opacity: 1 }, "-=0.1")
        .add(() => {
            // Swap visibility at the exact moment of landing
            TweenMax.set(mTarget, { opacity: 1 });
            TweenMax.set(mIntro, { opacity: 0 });
        })

        // 4. Stagger reveal the remaining letters of "Manshay"
        .staggerTo(anshay, 0.8, {
            opacity: 1,
            y: 0,
            ease: Power3.easeOut
        }, 0.05, "-=0.2");

    // 5. Final fade in subheading
    if (subheading) {
        tl.to(subheading, 1, {
            opacity: 1,
            y: 0,
            ease: Power2.easeOut
        }, "-=0.5");
    }

    tl.add(() => {
        // Cleanup: remove intro layer from DOM flow
        TweenMax.set(intro, { display: 'none' });
        // Make final layer relative instead of absolute to maintain layout
        TweenMax.set(final, { position: 'relative' });
        title.classList.add('animation-complete');
    });
}
