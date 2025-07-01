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
  carouselInterval = 20,
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

  const shinyTextSamples = normalizedShinyTexts.map(s => s.text || '');
  const maxShinyText = shinyTextSamples.reduce((a, b) => a.length > b.length ? a : b, '');
  const shinyTextRef = useRef(null);
  const [shinyWidth, setShinyWidth] = useState(0);

  useEffect(() => {
    if (shinyTextRef.current) {
      setShinyWidth(shinyTextRef.current.offsetWidth);
    }
  }, [maxShinyText]);

  // // Intersection observer logic 
  // useEffect(() => {
  //   if (!ref.current) return;
  //   const observer = new IntersectionObserver(
  //     ([entry]) => {
  //       if (entry.isIntersecting) {
  //         setPhase('base-animating');
  //         setCarouselIndex(-1);
  //         observer.unobserve(ref.current);
  //       }
  //     },
  //     { threshold, rootMargin }
  //   );
  //   observer.observe(ref.current);
  //   return () => observer.disconnect();
  //   // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [threshold, rootMargin]);

  // Carousel logic
  useEffect(() => {
    if (phase !== 'shiny-carousel') return;
    const total = normalizedShinyTexts.length;
    const interval = setTimeout(() => {
      setCarouselIndex((prev) => (prev < total - 1 ? prev + 1 : 0));
    }, carouselInterval);
    return () => clearTimeout(interval);
  }, [carouselIndex, normalizedShinyTexts.length, carouselInterval, phase]);

  // Animation keyframes and timing
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

  // Animation keyframes for shiny text
  const animateKeyframes = buildKeyframes(fromSnapshot, toSnapshots);
  const spanTransition = {
    duration: totalDuration,
    times,
    delay: 0,
  };
  spanTransition.ease = easing;

  return (
    <>
      {/* Hidden span to measure the widest shiny text */}
      <span
        ref={shinyTextRef}
        style={{
          position: 'absolute',
          visibility: 'hidden',
          whiteSpace: 'pre',
          fontWeight: 'inherit',
          fontSize: 'inherit',
          fontFamily: 'inherit',
        }}
      >
        {maxShinyText}
      </span>
      <p
        ref={ref}
        className={className}
        style={{ textAlign: 'center' }}
      >
        {/* Animate base text in, then render as static */}
        {phase === 'base-animating'
          ? elements.map((segment, index) => {
              const animateKeyframes = buildKeyframes(fromSnapshot, toSnapshots);
              const spanTransition = {
                duration: totalDuration,
                times,
                delay: (index * delay) / 1000,
              };
              spanTransition.ease = easing;
              return (
                <motion.span
                  className="inline-block will-change-[transform,filter,opacity]"
                  key={index}
                  initial={fromSnapshot}
                  animate={animateKeyframes}
                  transition={spanTransition}
                  onAnimationComplete={
                    index === elements.length - 1
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
                  {animateBy === 'words' && index < elements.length - 1 && '\u00A0'}
                </motion.span>
              );
            })
          : elements.map((segment, index) => (
              <span
                className="inline-block"
                key={index}
                style={{ marginRight: animateBy === 'words' && index < elements.length - 1 ? '0.25em' : undefined }}
              >
                {segment === ' ' ? '\u00A0' : segment}
                {animateBy === 'words' && index < elements.length - 1 && '\u00A0'}
              </span>
            ))}
        {/* Animate the shiny text only during the carousel phase, reserving space */}
        <span style={{ display: 'inline-block', width: shinyWidth, textAlign: 'left' }}>
          {phase === 'shiny-carousel' && normalizedShinyTexts[carouselIndex] && (
            <motion.span
              className="inline-block will-change-[transform,filter,opacity]"
              key={`shiny-text-${carouselIndex}`}
              initial={fromSnapshot}
              animate={buildKeyframes(fromSnapshot, toSnapshots)}
              transition={{
                duration: totalDuration,
                times,
                delay: 0,
                ease: easing,
              }}
              onAnimationComplete={onAnimationComplete}
            >
              <ShinyText {...normalizedShinyTexts[carouselIndex]} speed={normalizedShinyTexts[carouselIndex].speed ?? shinySpeed} />
            </motion.span>
          )}
        </span>
      </p>
    </>
  );
};

export default BlurText;