import { SCHOOL_ICONS } from "./mapConfig"
import type {
    DataDrivenPropertyValueSpecification,
    PropertyValueSpecification,
} from "maplibre-gl"

export const POINT_LAYER_STYLE = {
    paint: {
        "icon-color": [
            "interpolate",
            ["linear"],
            ["get", "score"],
            0,
            "#FF0000",
            50,
            "#FFFF00",
            100,
            "#00FF00",
        ] as DataDrivenPropertyValueSpecification<string>,
    },
    layout: {
        "icon-image": [
            "case",
            ["==", ["get", "nazwa", ["get", "typ"]], "Technikum"],
            SCHOOL_ICONS.Technikum,
            ["==", ["get", "nazwa", ["get", "typ"]], "Liceum ogólnokształcące"],
            SCHOOL_ICONS["Liceum ogólnokształcące"],
            ["==", ["get", "nazwa", ["get", "typ"]], "Szkoła podstawowa"],
            SCHOOL_ICONS["Szkoła podstawowa"],
            ["==", ["get", "nazwa", ["get", "typ"]], "Przedszkole"],
            SCHOOL_ICONS["Przedszkole"],
            // Default fallback for any other school types
            SCHOOL_ICONS.default,
        ] as DataDrivenPropertyValueSpecification<string>,
        "icon-overlap": "always" as PropertyValueSpecification<
            "always" | "never" | "cooperative"
        >,
    },
}

export const CLUSTER_LAYER_STYLE = {
    paint: {
        "circle-color": [
            "interpolate",
            ["linear"],
            [
                "case",
                [">", ["get", "nonZeroCount"], 0],
                ["/", ["get", "sum"], ["get", "nonZeroCount"]],
                0,
            ],
            0,
            "#FF0000", // red at 0
            50,
            "#FFFF00", // yellow at 50
            100,
            "#00FF00", // green at 100
        ] as DataDrivenPropertyValueSpecification<string>,
        "circle-radius": [
            "step",
            ["get", "point_count"],
            20,
            100,
            30,
            750,
            40,
        ] as DataDrivenPropertyValueSpecification<number>,
    },
    layout: {
        "text-field":
            "{point_count_abbreviated}" as PropertyValueSpecification<string>,
        "text-font": ["Noto Sans Regular"] as PropertyValueSpecification<
            string[]
        >,
        "text-size": 12 as PropertyValueSpecification<number>,
    },
}
