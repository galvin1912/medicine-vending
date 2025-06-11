import { useEffect } from 'react';

const useScrollToTop = (trigger = true, behavior = 'smooth', delay = 0) => {
  useEffect(() => {
    if (trigger) {
      const scrollToTop = () => {
        window.scrollTo({
          top: 0,
          left: 0,
          behavior: behavior
        });
      };

      if (delay > 0) {
        const timeoutId = setTimeout(scrollToTop, delay);
        return () => clearTimeout(timeoutId);
      } else {
        scrollToTop();
      }
    }
  }, [trigger, behavior, delay]);
};


export const useScrollToTopOnMount = (behavior = 'smooth') => {
  useEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: behavior
    });
  }, [behavior]);
};


export const useScrollToTopOnNavigate = (pathname, behavior = 'smooth') => {
  useEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: behavior
    });
  }, [pathname, behavior]);
};

export default useScrollToTop; 