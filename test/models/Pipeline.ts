/* tslint:disable */
/* eslint-disable */
/**
 * Nefryt LDS API
 * Database API for Nefryt LDS
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import {
    EditorPipeline,
    EditorPipelineFromJSON,
    EditorPipelineFromJSONTyped,
    EditorPipelineToJSON,
} from './EditorPipeline';

/**
 * 
 * @export
 * @interface Pipeline
 */
export interface Pipeline {
    /**
     * none
     * @type {number}
     * @memberof Pipeline
     */
    readonly iD: number;
    /**
     * none
     * @type {string}
     * @memberof Pipeline
     */
    name?: string;
    /**
     * none
     * @type {number}
     * @memberof Pipeline
     */
    beginPos?: number;
    /**
     * 
     * @type {EditorPipeline}
     * @memberof Pipeline
     */
    editorParams?: EditorPipeline;
}

export function PipelineFromJSON(json: any): Pipeline {
    return PipelineFromJSONTyped(json, false);
}

export function PipelineFromJSONTyped(json: any, ignoreDiscriminator: boolean): Pipeline {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'iD': json['ID'],
        'name': !exists(json, 'Name') ? undefined : json['Name'],
        'beginPos': !exists(json, 'BeginPos') ? undefined : json['BeginPos'],
        'editorParams': !exists(json, 'EditorParams') ? undefined : EditorPipelineFromJSON(json['EditorParams']),
    };
}

export function PipelineToJSON(value?: Pipeline | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'Name': value.name,
        'BeginPos': value.beginPos,
        'EditorParams': EditorPipelineToJSON(value.editorParams),
    };
}

