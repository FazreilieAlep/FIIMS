import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ProductComponent } from './p-metal/product/product.component';
import { ProductDetailsComponent } from './p-metal/product-details/product-details.component';
import { SupplierComponent } from './p-metal/supplier/supplier.component';
import { SupplierDetailsComponent } from './p-metal/supplier-details/supplier-details.component';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { PaginatorModule } from 'primeng/paginator';
import { DropdownModule } from 'primeng/dropdown';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TagModule } from "primeng/tag";
import { BreadcrumbModule } from 'primeng/breadcrumb';
import { MenuModule } from 'primeng/menu';
import { StyleClassModule } from 'primeng/styleclass';
import { ImageModule } from 'primeng/image';
import { GalleriaModule } from 'primeng/galleria';
import { CreateOrEditProductComponent } from './p-metal/create-or-edit-product/create-or-edit-product.component';
import { CheckboxModule } from 'primeng/checkbox';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { CreateOrEditProductModalComponent } from './p-metal/create-or-edit-product-modal/create-or-edit-product-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ProductComponent,
    ProductDetailsComponent,
    SupplierComponent,
    SupplierDetailsComponent,
    CreateOrEditProductComponent,
    CreateOrEditProductModalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ButtonModule,
    TableModule,
    PaginatorModule,
    DropdownModule,
    BrowserAnimationsModule,
    TagModule,
    BreadcrumbModule,
    MenuModule,
    StyleClassModule,
    ImageModule,
    GalleriaModule,
    CheckboxModule,
    MatCardModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
