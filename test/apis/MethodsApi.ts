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
    InlineResponse200,
    InlineResponse200FromJSON,
    InlineResponse200ToJSON,
    Method,
    MethodFromJSON,
    MethodToJSON,
    MethodParam,
    MethodParamFromJSON,
    MethodParamToJSON,
} from '../models';

export interface CreateMethodRequest {
    pipelineId: number;
    method?: Method;
}

export interface DeleteMethodByIdRequest {
    pipelineId: number;
    methodId: number;
}

export interface GetMethodByIdRequest {
    pipelineId: number;
    methodId: number;
}

export interface ListMethodParamsRequest {
    pipelineId: number;
    methodId: number;
}

export interface ListMethodsRequest {
    pipelineId: number;
}

export interface UpdateMethodRequest {
    pipelineId: number;
    methodId: number;
    method?: Method;
}

export interface UpdateMethodParamsRequest {
    pipelineId: number;
    methodId: number;
    methodParamDefId: string;
    methodParam?: Array<MethodParam>;
}

/**
 * 
 */
export class MethodsApi extends runtime.BaseAPI {

    /**
     * Creates a  method
     * Creates method
     */
    async createMethodRaw(requestParameters: CreateMethodRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Method>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling createMethod.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))),
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: MethodToJSON(requestParameters.method),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => MethodFromJSON(jsonValue));
    }

    /**
     * Creates a  method
     * Creates method
     */
    async createMethod(requestParameters: CreateMethodRequest, initOverrides?: RequestInit): Promise<Method> {
        const response = await this.createMethodRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Deletes specific  method
     * Deletes  method
     */
    async deleteMethodByIdRaw(requestParameters: DeleteMethodByIdRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Information>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling deleteMethodById.');
        }

        if (requestParameters.methodId === null || requestParameters.methodId === undefined) {
            throw new runtime.RequiredError('methodId','Required parameter requestParameters.methodId was null or undefined when calling deleteMethodById.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method/{methodId}`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))).replace(`{${"methodId"}}`, encodeURIComponent(String(requestParameters.methodId))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => InformationFromJSON(jsonValue));
    }

    /**
     * Deletes specific  method
     * Deletes  method
     */
    async deleteMethodById(requestParameters: DeleteMethodByIdRequest, initOverrides?: RequestInit): Promise<Information> {
        const response = await this.deleteMethodByIdRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Info for specific  method
     * Gets  method details
     */
    async getMethodByIdRaw(requestParameters: GetMethodByIdRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<InlineResponse200>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling getMethodById.');
        }

        if (requestParameters.methodId === null || requestParameters.methodId === undefined) {
            throw new runtime.RequiredError('methodId','Required parameter requestParameters.methodId was null or undefined when calling getMethodById.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method/{methodId}`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))).replace(`{${"methodId"}}`, encodeURIComponent(String(requestParameters.methodId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => InlineResponse200FromJSON(jsonValue));
    }

    /**
     * Info for specific  method
     * Gets  method details
     */
    async getMethodById(requestParameters: GetMethodByIdRequest, initOverrides?: RequestInit): Promise<InlineResponse200> {
        const response = await this.getMethodByIdRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * List all  method params
     * List pipelnie method params
     */
    async listMethodParamsRaw(requestParameters: ListMethodParamsRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Array<MethodParam>>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling listMethodParams.');
        }

        if (requestParameters.methodId === null || requestParameters.methodId === undefined) {
            throw new runtime.RequiredError('methodId','Required parameter requestParameters.methodId was null or undefined when calling listMethodParams.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method/{methodId}/param`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))).replace(`{${"methodId"}}`, encodeURIComponent(String(requestParameters.methodId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(MethodParamFromJSON));
    }

    /**
     * List all  method params
     * List pipelnie method params
     */
    async listMethodParams(requestParameters: ListMethodParamsRequest, initOverrides?: RequestInit): Promise<Array<MethodParam>> {
        const response = await this.listMethodParamsRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * List all methods
     * List pipelnie methods
     */
    async listMethodsRaw(requestParameters: ListMethodsRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Array<Method>>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling listMethods.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(MethodFromJSON));
    }

    /**
     * List all methods
     * List pipelnie methods
     */
    async listMethods(requestParameters: ListMethodsRequest, initOverrides?: RequestInit): Promise<Array<Method>> {
        const response = await this.listMethodsRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Updates  method
     * Updates method
     */
    async updateMethodRaw(requestParameters: UpdateMethodRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Method>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling updateMethod.');
        }

        if (requestParameters.methodId === null || requestParameters.methodId === undefined) {
            throw new runtime.RequiredError('methodId','Required parameter requestParameters.methodId was null or undefined when calling updateMethod.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method/{methodId}`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))).replace(`{${"methodId"}}`, encodeURIComponent(String(requestParameters.methodId))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: MethodToJSON(requestParameters.method),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => MethodFromJSON(jsonValue));
    }

    /**
     * Updates  method
     * Updates method
     */
    async updateMethod(requestParameters: UpdateMethodRequest, initOverrides?: RequestInit): Promise<Method> {
        const response = await this.updateMethodRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Put  method params
     * Put pipelnie method params
     */
    async updateMethodParamsRaw(requestParameters: UpdateMethodParamsRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<Information>> {
        if (requestParameters.pipelineId === null || requestParameters.pipelineId === undefined) {
            throw new runtime.RequiredError('pipelineId','Required parameter requestParameters.pipelineId was null or undefined when calling updateMethodParams.');
        }

        if (requestParameters.methodId === null || requestParameters.methodId === undefined) {
            throw new runtime.RequiredError('methodId','Required parameter requestParameters.methodId was null or undefined when calling updateMethodParams.');
        }

        if (requestParameters.methodParamDefId === null || requestParameters.methodParamDefId === undefined) {
            throw new runtime.RequiredError('methodParamDefId','Required parameter requestParameters.methodParamDefId was null or undefined when calling updateMethodParams.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/pipeline/{pipelineId}/method/{methodId}/param/{methodParamDefId}`.replace(`{${"pipelineId"}}`, encodeURIComponent(String(requestParameters.pipelineId))).replace(`{${"methodId"}}`, encodeURIComponent(String(requestParameters.methodId))).replace(`{${"methodParamDefId"}}`, encodeURIComponent(String(requestParameters.methodParamDefId))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: requestParameters.methodParam.map(MethodParamToJSON),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => InformationFromJSON(jsonValue));
    }

    /**
     * Put  method params
     * Put pipelnie method params
     */
    async updateMethodParams(requestParameters: UpdateMethodParamsRequest, initOverrides?: RequestInit): Promise<Information> {
        const response = await this.updateMethodParamsRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
