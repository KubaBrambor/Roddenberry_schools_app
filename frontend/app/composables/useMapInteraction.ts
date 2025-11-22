import type { Point } from "geojson"
import type { LngLatBounds } from "maplibre-gl"
import type maplibregl from "maplibre-gl"
import type { MapMouseLayerEvent } from "~/types/map"
import type {
    SzkolaPublicWithRelations,
    SzkolaPublicShortFromGeoJsonFeatures,
} from "~/types/schools"

export const useMapInteractions = (
    emit: (event: "point-clicked", school: SzkolaPublicWithRelations) => void,
    updateQueryBboxParam: (bounds: LngLatBounds) => void,
    displayPopup: Ref<boolean>,
    popupCoordinates: Ref<[number, number] | undefined>,
) => {
    let currentFeatureCoordinates: string | undefined = undefined
    let debounceTimeout: NodeJS.Timeout | null = null
    const hoveredSchool: Ref<SzkolaPublicShortFromGeoJsonFeatures | null> =
        ref(null)

    const handleMouseMove = (map: maplibregl.Map, e: MapMouseLayerEvent) => {
        const feature_collection = e.features?.[0]
        if (!feature_collection) return

        const pointGeometry = feature_collection.geometry as Point
        const featureCoordinates = pointGeometry.coordinates.toString()
        if (currentFeatureCoordinates !== featureCoordinates) {
            currentFeatureCoordinates = featureCoordinates

            // Change the cursor style as a UI indicator.
            map.getCanvas().style.cursor = "pointer"

            const coordinates = pointGeometry.coordinates.slice() as [
                number,
                number,
            ]
            // Update the hovered school data
            hoveredSchool.value =
                feature_collection.properties as SzkolaPublicShortFromGeoJsonFeatures

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
            }

            // Use the MglPopup component instead of native popup
            displayPopup.value = true
            popupCoordinates.value = coordinates
        }
    }

    const handleMouseLeave = (map: maplibregl.Map) => {
        currentFeatureCoordinates = undefined
        map.getCanvas().style.cursor = ""
        displayPopup.value = false
        popupCoordinates.value = undefined
        hoveredSchool.value = null
    }

    const handleClick = async (e: MapMouseLayerEvent) => {
        const feature_collection = e.features?.[0]
        if (!feature_collection) return

        const schoolFullDetails = await useApi<SzkolaPublicWithRelations>(
            `/schools/${feature_collection.properties.id}`,
        )

        if (schoolFullDetails.data.value) {
            emit("point-clicked", schoolFullDetails.data.value)
        }
    }

    const handleClusterClick = async (
        map: maplibregl.Map,
        e: MapMouseLayerEvent,
    ) => {
        const features = map.queryRenderedFeatures(e.point, {
            layers: ["clusters"],
        })
        const clusterId = features[0]?.properties.cluster_id
        const zoom = await map
            .getSource("schools-source")
            ?.getClusterExpansionZoom(clusterId)
        map.easeTo({
            center: features[0].geometry.coordinates,
            zoom,
        })
    }

    const handleMoveEnd = (map: maplibregl.Map) => {
        // Clear the previous timeout if it exists
        if (debounceTimeout) {
            clearTimeout(debounceTimeout)
        }

        // Set a new timeout
        debounceTimeout = setTimeout(() => {
            updateQueryBboxParam(map.getBounds())
        }, 300) // Wait for 300ms of inactivity before fetching
    }

    const setupMapEventHandlers = (map: maplibregl.Map) => {
        map.on("mousemove", "unclustered-points", (e) =>
            handleMouseMove(map, e),
        )
        map.on("mouseleave", "unclustered-points", () => handleMouseLeave(map))
        map.on("click", "unclustered-points", handleClick)
        map.on("click", "clusters", (e) => handleClusterClick(map, e))
        map.on("moveend", () => handleMoveEnd(map))
    }

    return { setupMapEventHandlers, hoveredSchool }
}
