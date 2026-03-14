import { useEffect, useRef, useState } from "react";

export function useIntersection<T extends HTMLElement = HTMLDivElement>() {
	const ref = useRef<T>(null);
	const [isIntersecting, setIsIntersecting] = useState(false);

	useEffect(() => {
		const element = ref.current;
		if (!element) return;

		const observer = new IntersectionObserver(
			([entry]) => {
				setIsIntersecting(entry.isIntersecting);
			},
			{
				root: null,
				rootMargin: "100px",
				threshold: 0,
			},
		);

		observer.observe(element);

		return () => observer.unobserve(element);
	}, []);

	return { ref, isIntersecting };
}
