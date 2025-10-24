import type { Feature, FeatureCollection, Point } from "geojson"
import type { SzkolaPublicShort } from "~/types/schools"

export const useSchoolGeoJson = (schools: Ref<SzkolaPublicShort[] | null>) => {
    const transformSchoolsToFeatures = (
        schools: SzkolaPublicShort[],
    ): Feature<Point, SzkolaPublicShort>[] => {
        return schools.map((school) => ({
            type: "Feature",
            properties: school,
            geometry: {
                type: "Point",
                coordinates: [
                    school.geolokalizacja_longitude,
                    school.geolokalizacja_latitude,
                ],
            },
        }))
    }

    const geoJsonSource = computed<FeatureCollection<Point, SzkolaPublicShort>>(
        () => {
            const features = schools.value
                ? transformSchoolsToFeatures(schools.value)
                : []

            return {
                type: "FeatureCollection",
                features,
            }
        },
    )

    return { geoJsonSource }
}
