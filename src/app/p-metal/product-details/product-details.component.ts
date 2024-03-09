import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit, Input } from '@angular/core';
import { PMetalService } from 'src/app/p-metal.service';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css'],
  changeDetection: ChangeDetectionStrategy.Default
})
export class ProductDetailsComponent implements OnInit {
  @Input() product: any = {};

  images: any[] | undefined;
  responsiveOptions: any[] | undefined;

  items: any[] = [];

  home: MenuItem | undefined;

  modalOpened2 = false;
  createProduct = false;

  constructor(
    private route: ActivatedRoute,
    private pMetalService: PMetalService,
    private location: Location,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.items.push({ label: 'Inventory', routerLink: '/pmetal/inventory' });
    this.items.push({ label: 'Product', routerLink: '/pmetal/inventory/' + Number(this.route.snapshot.paramMap.get('id')).toString() });

    this.home = { icon: 'pi pi-home', routerLink: '/home' };

    this.responsiveOptions = [
      {
        breakpoint: '1024px',
        numVisible: 5
      },
      {
        breakpoint: '768px',
        numVisible: 3
      },
      {
        breakpoint: '560px',
        numVisible: 1
      }
    ];

    this.loadProduct();

    this.cdr.detectChanges();
  }

  loadProduct(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.pMetalService.getProduct(id)
      .subscribe(product => {
        this.product = product;
        if (product.productName) {
          this.items.push({ label: product.productName, routerLink: '/pmetal/inventory/' + id.toString() });
          this.images = product.images;
          this.cdr.detectChanges();
        }
      });
  }

  openModal2(toEdit: boolean): void {
    if (this.modalOpened2 == false) {
      if (toEdit == true) {
        this.createProduct = false;
      } else {
        this.createProduct = true;
      }
      this.modalOpened2 = true;
    }
  }

  closeModal(): void {
    if (this.modalOpened2 == true) {
      this.modalOpened2 = false;
    }
  }
}
