import type maplibregl from "maplibre-gl"
export type MapMouseLayerEvent = maplibregl.MapMouseEvent & {
    features?: maplibregl.MapGeoJSONFeature[]
} & object
