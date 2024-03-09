import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { pmetal } from 'src/interface/pmetal';
import { pmetal_details } from 'src/interface/pmetal-details';
import { Observable, of } from 'rxjs';
import { supplier } from 'src/interface/supplier'
import { supplier_details } from 'src/interface/supplier-details'
import { catchError, map, tap } from 'rxjs/operators';

//import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class PMetalService {

  private pMetalUrl = "https://izz123.pythonanywhere.com/";  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private httpClient: HttpClient) { }

  /** GET products from the server */
  getProducts(): Observable<pmetal[]> {
    const products = this.httpClient.get<pmetal[]>(this.pMetalUrl + "api/precious-metal/inventory");
    return products;
  }

  /** GET product from the server based on productID*/
  getProduct(id: number): Observable<pmetal_details> {
    const url = `api/precious-metal/inventory/${id}`;
    const product = this.httpClient.get<pmetal_details>(this.pMetalUrl + url);
    return product;
  }

  /** GET suppliers from the server */
  getSuppliers(): Observable<supplier[]> {
    const suppliers = this.httpClient.get<supplier[]>(this.pMetalUrl + "api/precious-metal/supplier");
    return suppliers;
  }

  /** GET product from the server based on productID*/
  getSupplier(id: number): Observable<supplier_details> {
    const url = `api/precious-metal/supplier/${id}`;
    const supplier = this.httpClient.get<supplier_details>(this.pMetalUrl + url);
    return supplier;
  }

}
