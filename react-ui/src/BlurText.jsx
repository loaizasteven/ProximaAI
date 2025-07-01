import { motion } from 'framer-motion';
import { useEffect, useRef, useState, useMemo } from 'react';
import ShinyText from './ShinyText';

const buildKeyframes = (from, steps) => {
  const keys = new Set([
    ...Object.keys(from),
    ...steps.flatMap((s) => Object.keys(s)),
  ]);

  const keyframes = {};
  keys.forEach((k) => {
    keyframes[k] = [from[k], ...steps.map((s) => s[k])];
  });
  return keyframes;
};

const BlurText = ({
  text = '',
  shinyTexts = [],
  shinySpeed = 10,
  delay = 200,
  className = '',
  animateBy = 'words',
  direction = 'top',
  threshold = 0.1,
  rootMargin = '0px',
  animationFrom,
  animationTo,
  easing = (t) => t,
  onAnimationComplete,
  stepDuration = 0.35,
  carouselInterval = 2000,
}) => {
  const elements = animateBy === 'words' ? text.split(' ') : text.split('');
  const [phase, setPhase] = useState('base-animating');
  const [carouselIndex, setCarouselIndex] = useState(-1);
  const ref = useRef(null);
  const baseStaticPause = 1000; // ms to keep base text static before shiny carousel

  // Normalize shinyTexts to always be an array of objects
  const normalizedShinyTexts = shinyTexts.map((s) =>
    typeof s === 'string' ? { text: s } : s
  );

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setCarouselIndex(0);
          observer.unobserve(ref.current);
        }
      },
      { threshold, rootMargin }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [threshold, rootMargin]);

  useEffect(() => {
    if (phase !== 'shiny-carousel') return;
    const total = normalizedShinyTexts.length;
    const interval = setTimeout(() => {
      setCarouselIndex((prev) => (prev < total - 1 ? prev + 1 : 0));
    }, carouselInterval);
    return () => clearTimeout(interval);
  }, [carouselIndex, normalizedShinyTexts.length, carouselInterval, phase]);

  const defaultFrom = useMemo(
    () =>
      direction === 'top'
        ? { filter: 'blur(10px)', opacity: 0, y: -50 }
        : { filter: 'blur(10px)', opacity: 0, y: 50 },
    [direction]
  );

  const defaultTo = useMemo(
    () => [
      {
        filter: 'blur(5px)',
        opacity: 0.5,
        y: direction === 'top' ? 5 : -5,
      },
      { filter: 'blur(0px)', opacity: 1, y: 0 },
    ],
    [direction]
  );

  const fromSnapshot = animationFrom ?? defaultFrom;
  const toSnapshots = animationTo ?? defaultTo;

  const stepCount = toSnapshots.length + 1;
  const totalDuration = stepDuration * (stepCount - 1);
  const times = Array.from({ length: stepCount }, (_, i) =>
    stepCount === 1 ? 0 : i / (stepCount - 1)
  );

  let elementsWithShiny = [];
  if (phase === 'base-animating' || phase === 'base-static') {
    elementsWithShiny = [...elements];
  } else if (phase === 'shiny-carousel' && normalizedShinyTexts[carouselIndex]) {
    elementsWithShiny = [`__SHINY__${carouselIndex}`];
  }

  return (
    <>
      <p
        ref={ref}
        className={className}
        style={{ display: 'flex', flexWrap: 'wrap' }}
      >
        {elementsWithShiny.map((segment, index) => {
          const animateKeyframes = buildKeyframes(fromSnapshot, toSnapshots);

          const spanTransition = {
            duration: totalDuration,
            times,
            delay: (index * delay) / 1000,
          };
          spanTransition.ease = easing;

          const shinyMatch = /^__SHINY__(\d+)$/.exec(segment);
          if (shinyMatch) {
            const shinyIdx = parseInt(shinyMatch[1], 10);
            const shinyProps = normalizedShinyTexts[shinyIdx] || {};
            const speed = shinyProps.speed !== undefined ? shinyProps.speed : shinySpeed;
            return (
              <motion.span
                className="inline-block will-change-[transform,filter,opacity]"
                key={`shiny-text-${shinyIdx}`}
                initial={fromSnapshot}
                animate={animateKeyframes}
                transition={spanTransition}
                onAnimationComplete={onAnimationComplete}
              >
                <ShinyText {...shinyProps} speed={speed} />
              </motion.span>
            );
          }

          return (
            <motion.span
              className="inline-block will-change-[transform,filter,opacity]"
              key={index}
              initial={fromSnapshot}
              animate={phase === 'base-animating' ? animateKeyframes : fromSnapshot}
              transition={spanTransition}
              onAnimationComplete={
                phase === 'base-animating' && index === elementsWithShiny.length - 1
                  ? () => {
                      setPhase('base-static');
                      setTimeout(() => {
                        setPhase('shiny-carousel');
                        setCarouselIndex(0);
                      }, baseStaticPause);
                    }
                  : undefined
              }
            >
              {segment === ' ' ? '\u00A0' : segment}
              {animateBy === 'words' && index < elementsWithShiny.length - 1 && '\u00A0'}
            </motion.span>
          );
        })}
      </p>
    </>
  );
};

export default BlurText;