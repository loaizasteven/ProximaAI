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
  shinyText = '',
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
}) => {
  const elements = animateBy === 'words' ? text.split(' ') : text.split('');
  const elementsWithShiny = [...elements, '__SHINY__'];
  const [inView, setInView] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.unobserve(ref.current);
        }
      },
      { threshold, rootMargin }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [threshold, rootMargin]);

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

          if (segment === '__SHINY__') {
            return (
              <motion.span
                className="inline-block will-change-[transform,filter,opacity]"
                key="shiny-text"
                initial={fromSnapshot}
                animate={inView ? animateKeyframes : fromSnapshot}
                transition={spanTransition}
                onAnimationComplete={onAnimationComplete}
              >
                <ShinyText text={shinyText} disabled={false} speed={shinySpeed} className='custom-class' />
              </motion.span>
            );
          }

          return (
            <motion.span
              className="inline-block will-change-[transform,filter,opacity]"
              key={index}
              initial={fromSnapshot}
              animate={inView ? animateKeyframes : fromSnapshot}
              transition={spanTransition}
              onAnimationComplete={
                index === elementsWithShiny.length - 1 ? onAnimationComplete : undefined
              }
            >
              {segment === ' ' ? '\u00A0' : segment}
              {animateBy === 'words' && index < elementsWithShiny.length - 2 && '\u00A0'}
            </motion.span>
          );
        })}
      </p>
    </>
  );
};

export default BlurText;