import type { BoundingBox } from "./boundingBox"

/**
 * Voivodeship data structure containing name and bounding box coordinates
 */
export interface VoivodeshipData {
    name: string
    coordinates: BoundingBox
}
