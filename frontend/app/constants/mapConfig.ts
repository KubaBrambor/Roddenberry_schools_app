import triangleIconUrl from "~/assets/images/figures/triangle.png"
import diamondIconUrl from "~/assets/images/figures/diamond.png"
import squareIconUrl from "~/assets/images/figures/square.png"
import starIconUrl from "~/assets/images/figures/star.png"
import hexagonIconUrl from "~/assets/images/figures/hexagon.png"

// constants/mapConfig.ts
export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
    defaultCenter: [21.008333, 52.232222] as [number, number],
    defaultZoom: 12,
    polandBounds: [
        [14.0, 49],
        [24.5, 55.2],
    ] as [[number, number], [number, number]],
    warsawBounds: [
        [20.7639, 52.1189],
        [21.3901, 52.3473],
    ] as [[number, number], [number, number]],
}

export const SCHOOL_ICONS = {
    Technikum: "triangle_sdf",
    "Liceum ogólnokształcące": "diamond_sdf",
    "Szkoła podstawowa": "square_sdf",
    Przedszkole: "hexagon_sdf",
    default: "star_sdf",
}

export const ICON_URLS = [
    triangleIconUrl,
    diamondIconUrl,
    squareIconUrl,
    starIconUrl,
    hexagonIconUrl,
]
