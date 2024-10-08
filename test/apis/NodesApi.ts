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


import * as runtime from '../runtime';
import {
    Information,
    InformationFromJSON,
    InformationToJSON,
    Node,
    NodeFromJSON,
    NodeToJSON,
} from '../models';

export interface CreateNodeRequest {
    node?: Node;
}

export interface DeleteNodeByIdRequest {
    nodeId: number;
}

export interface GetNodeByIdRequest {
    nodeId: number;
}

export interface UpdateNodeRequest {
    nodeId: number;
    node?: Node;
}

/**
 * 
 */
export class NodesApi extends runtime.BaseAPI {

    /**
     * Create a nodes
     * Create nodes
     */
    async createNodeRaw(requestParameters: CreateNodeRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Node>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/node`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: NodeToJSON(requestParameters.node),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => NodeFromJSON(jsonValue));
    }

    /**
     * Create a nodes
     * Create nodes
     */
    async createNode(requestParameters: CreateNodeRequest = {}, initOverrides?: RequestInit): Promise<Node> {
        const response = await this.createNodeRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Deletes specific node
     * Deletes node
     */
    async deleteNodeByIdRaw(requestParameters: DeleteNodeByIdRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Information>> {
        if (requestParameters.nodeId === null || requestParameters.nodeId === undefined) {
            throw new runtime.RequiredError('nodeId','Required parameter requestParameters.nodeId was null or undefined when calling deleteNodeById.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/node/{nodeId}`.replace(`{${"nodeId"}}`, encodeURIComponent(String(requestParameters.nodeId))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => InformationFromJSON(jsonValue));
    }

    /**
     * Deletes specific node
     * Deletes node
     */
    async deleteNodeById(requestParameters: DeleteNodeByIdRequest, initOverrides?: RequestInit): Promise<Information> {
        const response = await this.deleteNodeByIdRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Info for specific node
     * Gets node details
     */
    async getNodeByIdRaw(requestParameters: GetNodeByIdRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Node>> {
        if (requestParameters.nodeId === null || requestParameters.nodeId === undefined) {
            throw new runtime.RequiredError('nodeId','Required parameter requestParameters.nodeId was null or undefined when calling getNodeById.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/node/{nodeId}`.replace(`{${"nodeId"}}`, encodeURIComponent(String(requestParameters.nodeId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => NodeFromJSON(jsonValue));
    }

    /**
     * Info for specific node
     * Gets node details
     */
    async getNodeById(requestParameters: GetNodeByIdRequest, initOverrides?: RequestInit): Promise<Node> {
        const response = await this.getNodeByIdRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * List all nodes
     * List nodes
     */
    async listNodesRaw(initOverrides?: RequestInit): Promise<runtime.ApiResponse<Array<Node>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/node`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(NodeFromJSON));
    }

    /**
     * List all nodes
     * List nodes
     */
    async listNodes(initOverrides?: RequestInit): Promise<Array<Node>> {
        const response = await this.listNodesRaw(initOverrides);
        return await response.value();
    }

    /**
     * Updates a nodes
     * Updates nodes
     */
    async updateNodeRaw(requestParameters: UpdateNodeRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Node>> {
        if (requestParameters.nodeId === null || requestParameters.nodeId === undefined) {
            throw new runtime.RequiredError('nodeId','Required parameter requestParameters.nodeId was null or undefined when calling updateNode.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/node/{nodeId}`.replace(`{${"nodeId"}}`, encodeURIComponent(String(requestParameters.nodeId))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: NodeToJSON(requestParameters.node),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => NodeFromJSON(jsonValue));
    }

    /**
     * Updates a nodes
     * Updates nodes
     */
    async updateNode(requestParameters: UpdateNodeRequest, initOverrides?: RequestInit): Promise<Node> {
        const response = await this.updateNodeRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
