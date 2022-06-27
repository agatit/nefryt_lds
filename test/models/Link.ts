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
/**
 * 
 * @export
 * @interface Link
 */
export interface Link {
    /**
     * none
     * @type {number}
     * @memberof Link
     */
    readonly iD: number;
    /**
     * none
     * @type {number}
     * @memberof Link
     */
    beginNodeID?: number;
    /**
     * none
     * @type {number}
     * @memberof Link
     */
    endNodeID?: number;
    /**
     * none
     * @type {number}
     * @memberof Link
     */
    length?: number;
}

export function LinkFromJSON(json: any): Link {
    return LinkFromJSONTyped(json, false);
}

export function LinkFromJSONTyped(json: any, ignoreDiscriminator: boolean): Link {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'iD': json['ID'],
        'beginNodeID': !exists(json, 'BeginNodeID') ? undefined : json['BeginNodeID'],
        'endNodeID': !exists(json, 'EndNodeID') ? undefined : json['EndNodeID'],
        'length': !exists(json, 'Length') ? undefined : json['Length'],
    };
}

export function LinkToJSON(value?: Link | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'BeginNodeID': value.beginNodeID,
        'EndNodeID': value.endNodeID,
        'Length': value.length,
    };
}

