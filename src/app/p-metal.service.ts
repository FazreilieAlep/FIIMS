import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { pmetal } from 'src/interface/pmetal';
import { pmetal_details } from 'src/interface/pmetal-details';
import { Observable, throwError } from 'rxjs';
import { supplier } from 'src/interface/supplier'
import { supplier_details } from 'src/interface/supplier-details'
import { catchError, } from 'rxjs/operators';
import { instrument } from '../interface/instrument';
import { instrument_details } from '../interface/instrument-details';

//import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class PMetalService {

  private url = "https://izz123.pythonanywhere.com/";  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private httpClient: HttpClient) { }

  // PMETAL API SERVICE
  /** GET products from the server */
  getProducts(): Observable<pmetal[]> {
    const products = this.httpClient.get<pmetal[]>(this.url + "api/precious-metal/inventory");
    return products;
  }

  /** GET product from the server based on productID*/
  getProduct(id: number): Observable<pmetal_details> {
    const url = `api/precious-metal/inventory/${id}`;
    const product = this.httpClient.get<pmetal_details>(this.url + url);
    return product;
  }

  /** GET suppliers from the server */
  getSuppliers(): Observable<supplier[]> {
    const suppliers = this.httpClient.get<supplier[]>(this.url + "api/precious-metal/supplier");
    return suppliers;
  }

  /** GET product from the server based on productID*/
  getSupplier(id: number): Observable<supplier_details> {
    const url = `api/precious-metal/supplier/${id}`;
    const supplier = this.httpClient.get<supplier_details>(this.url + url);
    return supplier;
  }

  /** ADD new product */
  addProduct(obj: object): Observable<pmetal_details> {
    const url = `api/precious-metal/add-inventory`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  /** REMOVE product */
  deleteProduct(obj: pmetal): Observable<pmetal> {
    const url = `api/precious-metal/delete-inventory`;
    const dataPass = { productName: obj.productName, productID: obj.productID };
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  updateProduct(obj: object): Observable<any> {
    const url = '/api/precious-metal/update-inventory'; // Relative URL
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  /** ADD new Supplier */
  addSupplier(obj: object): Observable<supplier> {
    const url = `api/precious-metal/add-supplier`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  updateSupplier(obj: object): Observable<supplier> {
    const url = `api/precious-metal/update-supplier`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  deleteSupplier(obj: object): Observable<supplier> {
    const url = `api/precious-metal/delete-supplier`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  // MINSTRUMENT API SERVICE
  /** GET instruments from the server */
  getInstruments(): Observable<instrument[]> {
    const instruments = this.httpClient.get<instrument[]>(this.url + "api/musical-instrument/inventory");
    return instruments;
  }

  /** GET product from the server based on productID*/
  getInstrument(id: number): Observable<instrument_details> {
    const url = `api/musical-instrument/inventory/${id}`;
    const product = this.httpClient.get<instrument_details>(this.url + url);
    return product;
  }

  /** GET musical instrument suppliers from the server */
  getInstrumentSuppliers(): Observable<supplier[]> {
    const suppliers = this.httpClient.get<supplier[]>(this.url + "api/musical-instrument/supplier");
    return suppliers;
  }

  /** ADD new Supplier */
  addInstrumentSupplier(obj: object): Observable<supplier> {
    const url = `api/musical-instrument/add-supplier`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  updateInstrumentSupplier(obj: object): Observable<supplier> {
    const url = `api/musical-instrument/update-supplier`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }

  deleteInstrumentSupplier(obj: object): Observable<supplier> {
    const url = `api/musical-instrument/delete-supplier`;
    return this.httpClient.post<any>(this.url + url, obj)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          let errorMessage = '';
          if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
          } else {
            // Backend error
            errorMessage = `Error: ${error.status}, ${error.error}`;
          }
          return throwError(errorMessage);
        })
      );
  }
}
