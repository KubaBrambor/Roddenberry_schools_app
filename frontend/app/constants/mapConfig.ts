import triangleIconUrl from "~/assets/images/figures/triangle.png"
import diamondIconUrl from "~/assets/images/figures/diamond.png"
import squareIconUrl from "~/assets/images/figures/square.png"
import starIconUrl from "~/assets/images/figures/star.png"
import hexagonIconUrl from "~/assets/images/figures/hexagon.png"
import type { LngLatBoundsLike } from "maplibre-gl"

// constants/mapConfig.ts
export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
    defaultCenter: [19, 52] as [number, number],
    defaultZoom: 8,
    polandBounds: [
        [14.0, 49],
        [24.5, 55.2],
    ] as LngLatBoundsLike,
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
