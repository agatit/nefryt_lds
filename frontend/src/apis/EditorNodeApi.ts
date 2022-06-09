// tslint:disable
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


import { HttpMethods, QueryConfig, ResponseBody, ResponseText } from 'redux-query';
import * as runtime from '../runtime';
import {
    EditorNode,
    EditorNodeFromJSON,
    EditorNodeToJSON,
    Information,
    InformationFromJSON,
    InformationToJSON,
} from '../models';

export interface EditorNodeCreateNodesRequest {
    editorNode?: Array<EditorNode>;
}

export interface EditorNodeDeleteEditorNodeByIdRequest {
    editorNodeId: number;
}

export interface EditorNodeDeleteEditorNodesRequest {
    editorNode?: Array<EditorNode>;
}

export interface EditorNodeGetEditorNodeByIdRequest {
    editorNodeId: number;
}


/**
 * Create a editor nodes
 * Create editor nodes
 */
function editorNodeCreateNodesRaw<T>(requestParameters: EditorNodeCreateNodesRequest, requestConfig: runtime.TypedQueryConfig<T, Information> = {}): QueryConfig<T> {
    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};

    headerParameters['Content-Type'] = 'application/json';


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/editor/node`,
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'POST',
            headers: headerParameters,
        },
        body: queryParameters || requestParameters.editorNode?.map(EditorNodeToJSON),
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(InformationFromJSON(body), text);
    }

    return config;
}

/**
* Create a editor nodes
* Create editor nodes
*/
export function editorNodeCreateNodes<T>(requestParameters: EditorNodeCreateNodesRequest, requestConfig?: runtime.TypedQueryConfig<T, Information>): QueryConfig<T> {
    return editorNodeCreateNodesRaw(requestParameters, requestConfig);
}

/**
 * Delete specific editor node
 * Detail editor node
 */
function editorNodeDeleteEditorNodeByIdRaw<T>(requestParameters: EditorNodeDeleteEditorNodeByIdRequest, requestConfig: runtime.TypedQueryConfig<T, Information> = {}): QueryConfig<T> {
    if (requestParameters.editorNodeId === null || requestParameters.editorNodeId === undefined) {
        throw new runtime.RequiredError('editorNodeId','Required parameter requestParameters.editorNodeId was null or undefined when calling editorNodeDeleteEditorNodeById.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/editor/node/{editorNodeId}`.replace(`{${"editorNodeId"}}`, encodeURIComponent(String(requestParameters.editorNodeId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'DELETE',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(InformationFromJSON(body), text);
    }

    return config;
}

/**
* Delete specific editor node
* Detail editor node
*/
export function editorNodeDeleteEditorNodeById<T>(requestParameters: EditorNodeDeleteEditorNodeByIdRequest, requestConfig?: runtime.TypedQueryConfig<T, Information>): QueryConfig<T> {
    return editorNodeDeleteEditorNodeByIdRaw(requestParameters, requestConfig);
}

/**
 * Delete editor nodes
 * Detail editor nodes
 */
function editorNodeDeleteEditorNodesRaw<T>(requestParameters: EditorNodeDeleteEditorNodesRequest, requestConfig: runtime.TypedQueryConfig<T, Information> = {}): QueryConfig<T> {
    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};

    headerParameters['Content-Type'] = 'application/json';


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/editor/node`,
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'DELETE',
            headers: headerParameters,
        },
        body: queryParameters || requestParameters.editorNode?.map(EditorNodeToJSON),
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(InformationFromJSON(body), text);
    }

    return config;
}

/**
* Delete editor nodes
* Detail editor nodes
*/
export function editorNodeDeleteEditorNodes<T>(requestParameters: EditorNodeDeleteEditorNodesRequest, requestConfig?: runtime.TypedQueryConfig<T, Information>): QueryConfig<T> {
    return editorNodeDeleteEditorNodesRaw(requestParameters, requestConfig);
}

/**
 * Info for specific editor node
 * Detail editor node
 */
function editorNodeGetEditorNodeByIdRaw<T>(requestParameters: EditorNodeGetEditorNodeByIdRequest, requestConfig: runtime.TypedQueryConfig<T, EditorNode> = {}): QueryConfig<T> {
    if (requestParameters.editorNodeId === null || requestParameters.editorNodeId === undefined) {
        throw new runtime.RequiredError('editorNodeId','Required parameter requestParameters.editorNodeId was null or undefined when calling editorNodeGetEditorNodeById.');
    }

    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/editor/node/{editorNodeId}`.replace(`{${"editorNodeId"}}`, encodeURIComponent(String(requestParameters.editorNodeId))),
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(EditorNodeFromJSON(body), text);
    }

    return config;
}

/**
* Info for specific editor node
* Detail editor node
*/
export function editorNodeGetEditorNodeById<T>(requestParameters: EditorNodeGetEditorNodeByIdRequest, requestConfig?: runtime.TypedQueryConfig<T, EditorNode>): QueryConfig<T> {
    return editorNodeGetEditorNodeByIdRaw(requestParameters, requestConfig);
}

/**
 * List all editor nodes
 * List editor nodes
 */
function editorNodeListNodesRaw<T>( requestConfig: runtime.TypedQueryConfig<T, Array<EditorNode>> = {}): QueryConfig<T> {
    let queryParameters = null;


    const headerParameters : runtime.HttpHeaders = {};


    const { meta = {} } = requestConfig;

    const config: QueryConfig<T> = {
        url: `${runtime.Configuration.basePath}/editor/node`,
        meta,
        update: requestConfig.update,
        queryKey: requestConfig.queryKey,
        optimisticUpdate: requestConfig.optimisticUpdate,
        force: requestConfig.force,
        rollback: requestConfig.rollback,
        options: {
            method: 'GET',
            headers: headerParameters,
        },
        body: queryParameters,
    };

    const { transform: requestTransform } = requestConfig;
    if (requestTransform) {
        config.transform = (body: ResponseBody, text: ResponseBody) => requestTransform(body.map(EditorNodeFromJSON), text);
    }

    return config;
}

/**
* List all editor nodes
* List editor nodes
*/
export function editorNodeListNodes<T>( requestConfig?: runtime.TypedQueryConfig<T, Array<EditorNode>>): QueryConfig<T> {
    return editorNodeListNodesRaw( requestConfig);
}

