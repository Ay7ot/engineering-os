# Motion Recipes

Library choice first: `motion/react` (formerly Framer Motion) is the default for
UI, bento and state-change motion. GSAP plus ScrollTrigger is for full-page
scrolltelling and scroll hijacks, isolated in a leaf component with `useEffect`
cleanup. Three.js or WebGL is for canvas and 3D scenes, isolated the same way.
Never mix GSAP or Three.js with Motion in the same component tree; they fight
over the same frames.

## Forbidden animation patterns
- `window.addEventListener("scroll", ...)`: runs on every scroll frame, jank
  prone, no batching. Use `useScroll()`, ScrollTrigger, IntersectionObserver or
  CSS scroll-driven animations (`animation-timeline: view()`).
- Custom scroll progress math from `window.scrollY` held in component state, for
  the same reason: it re-renders every frame.
- `requestAnimationFrame` loops that touch component state. Use motion values
  (`useMotionValue` plus `useTransform`) instead.
- Layout props on static content just in case; they cost measurement work. Use
  `layout` and `layoutId` only for visible re-ordering, expanding modals and
  shared elements.
- Animated `top`, `left`, `width` or `height`. Animate `transform` and `opacity`
  only, and use `will-change: transform` sparingly.

## Scroll reveal stagger (default)
Use Motion `whileInView` for "items appear as they enter the viewport". Lighter
than ScrollTrigger, no plugin. Save GSAP for real pin and scrub work.

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

## Sticky stack (cards pin and stack on scroll)
The classic failure: the trigger fires halfway through the scroll instead of
pinning at the viewport top. The fix is `start: "top top"`.

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center">
          {card}
        </div>
      ))}
    </div>
  );
}
```

Every card except the last is pinned, and the scale and opacity transform is
driven by the NEXT card's trigger, so the previous card shrinks as the next one
arrives.

## Horizontal pan (vertical scroll drives a horizontal track)
The classic failure: the animation starts before the section is pinned, so the
user sees half a slide. Pin the wrapper, scrub the inner track.

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

## Reduced motion
Any motion above intensity 3 honors `prefers-reduced-motion`. With Motion, wrap
in `useReducedMotion()` and degrade to static. In CSS, gate animations behind
`@media (prefers-reduced-motion: no-preference)`, or disable them under
`@media (prefers-reduced-motion: reduce)`. Loops, parallax, scroll hijack and
magnetic physics always collapse to static or instant.
