export const useScoreColor = () => {
    const getColor = (score: number) => {
        if (score <= 50) {
            // Red to Yellow (0-50)
            const ratio = score / 50
            const r = 200
            const g = Math.round(200 * ratio)
            return `rgb(${r}, ${g},0)`
        }
        // Yellow to Dark Green (50-100)
        const ratio = (score - 50) / 50
        const r = Math.round(200 * (1 - ratio))
        const g = Math.round(200 - 100 * ratio)
        return `rgb(${r}, ${g},0)`
    }

    return { getColor }
}
