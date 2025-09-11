export const useMapUtils = () => {

    const getColorForValue = (value: number): string => {
        const clampedValue = Math.max(0, Math.min(100, value));
        const red = clampedValue < 50 ? 255 : Math.round(255 - ((clampedValue - 50) * 5.1));
        const green = clampedValue > 50 ? 255 : Math.round(clampedValue * 5.1);
        return `rgb(${red},${green},0)`;
    };

    const getShapeSVG = (type: string): string => {
        switch (type) {
            case "Technikum":
                return "<rect width='24' height='24' style='fill:currentColor;stroke:black;stroke-width:1;'/>"; 
            case "Liceum":
                return "<circle cx='12' cy='12' r='11' style='fill:currentColor;stroke:black;stroke-width:1;'/>";
            case "Zawodowka":
            case "Szkoła zawodowa":
                return "<polygon points='12,2 22,22 2,22' style='fill:currentColor;stroke:black;stroke-width:1;'/>";
            default:
                return "<circle cx='12' cy='12' r='11' style='fill:currentColor;stroke:black;stroke-width:1;'/>";
        }
    };

    return {
        getColorForValue,
        getShapeSVG
    };
};