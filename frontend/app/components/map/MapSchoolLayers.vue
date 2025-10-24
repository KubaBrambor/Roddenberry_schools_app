<script setup lang="ts">
import type { FeatureCollection, Point } from "geojson"
import {
    CLUSTER_LAYER_STYLE,
    POINT_LAYER_STYLE,
} from "~/constants/mapLayerStyles"
import type { SzkolaPublicShort } from "~/types/schools"

defineProps<{
    sourceData: FeatureCollection<Point, SzkolaPublicShort>
}>()
</script>

<template>
    <MglGeoJsonSource
        source-id="schools-source"
        :data="sourceData"
        :cluster="true"
        :cluster-properties="{
            sum: ['+', ['get', 'score']],
            nonZeroCount: ['+', ['case', ['>', ['get', 'score'], 0], 1, 0]],
        }">
        <MglSymbolLayer
            layer-id="unclustered-points"
            source="schools-source"
            :filter="['!', ['has', 'point_count']]"
            :paint="POINT_LAYER_STYLE.paint"
            :layout="POINT_LAYER_STYLE.layout" />

        <MglCircleLayer
            layer-id="clusters"
            source="schools-source"
            :filter="['has', 'cluster']"
            :paint="CLUSTER_LAYER_STYLE.paint" />

        <MglSymbolLayer
            layer-id="cluster-count"
            source="schools-source"
            :filter="['has', 'cluster']"
            :layout="CLUSTER_LAYER_STYLE.layout" />
    </MglGeoJsonSource>
</template>
