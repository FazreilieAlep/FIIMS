import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { PMetalService } from 'src/app/p-metal.service'
import { supplier } from 'src/interface/supplier'
import { pmetal } from '../../../interface/pmetal';

interface image {
  link: string;
  edit: boolean;
}

@Component({
  selector: 'app-create-or-edit-product-modal',
  templateUrl: './create-or-edit-product-modal.component.html',
  styleUrls: ['./create-or-edit-product-modal.component.css']
})
export class CreateOrEditProductModalComponent implements OnInit{
  @Input() createProduct: boolean = false;
  @Input() editProduct: any;

  @Output() closeModal = new EventEmitter<void>();
  @Output() updateTable = new EventEmitter<void>();

  initialEditProductData: any;
  enableEdit: any = true;

  image: string = '';
  images: image[] = [];
  productName = "";
  premium = 0.00;
  quantity = 0;
  year = 0;
  weight = 0.00;

  selectedSupplier: supplier | undefined;

  formGroup!: FormGroup;

  suppliers: supplier[] = [];

  metals: any[] = [
    { name: 'gold', key: '1' },
    { name: 'silver', key: '2' }
  ];

  categories: any[] = [
    { name: 'coin', key: '1' },
    { name: 'bar', key: '2' }
  ];

  measurements: any[] = [
    { name: 'g', key: '1' },
    { name: 'kg', key: '2' },
    { name: 'oz', key: '3' }
  ];

  saveButtonClicked: boolean = false;

  constructor(
    private pMetalService: PMetalService) { }

  ngOnInit() {
    this.loadSuppliers();
    this.formGroup = new FormGroup({
      selectedCategory: new FormControl(),
      selectedMetal: new FormControl(),
      selectedMeasurement: new FormControl()
    });
    if (this.createProduct == false && this.editProduct) {
      this.enableEdit = false;
      if (this.editProduct.images) {
        for (const image of this.editProduct.images) {
          this.images.push({ link: image.itemImageSrc, edit: false });
        }
      }
      // Initialize form controls based on editProduct data
      this.productName = this.editProduct.productName;
      this.selectedSupplier = this.editProduct.supplierName;
      this.quantity = this.editProduct.quantity;
      this.year = this.editProduct.year;
      this.weight = this.editProduct.weight;
      this.premium = this.editProduct.premium;

      // Initialize selectedMeasurement
      const selectedMeasurement = this.measurements.find(measurement => measurement.name === this.editProduct.measurement);
      this.formGroup.get('selectedMeasurement')?.setValue(selectedMeasurement);

      // Initialize selectedMetal
      const selectedMetal = this.metals.find(metal => metal.name === this.editProduct.metal);
      this.formGroup.get('selectedMetal')?.setValue(selectedMetal);

      // Initialize selectedCategory
      const selectedCategory = this.categories.find(category => category.name === this.editProduct.category);
      this.formGroup.get('selectedCategory')?.setValue(selectedCategory);

      this.initialEditProductData = {
        productID: this.editProduct.productID,
        supplierName: this.editProduct.supplierName,
        productName: this.productName,
        premium: this.premium,
        category: this.formGroup.get('selectedCategory')?.value['name'],
        metal: this.formGroup.get('selectedMetal')?.value['name'],
        year: this.year,
        measurement: this.formGroup.get('selectedMeasurement')?.value['name'],
        weight: this.weight,
        quantity: this.quantity,
        images: this.images.map(image => image.link)
      }
    }
  }

  enableEditButton() {
    if (!this.enableEdit) {
      this.enableEdit = true;
    } else {
      this.enableEdit = false;
    }
    
  }

  loadSuppliers(): void {
    this.pMetalService.getSuppliers()
      .subscribe(suppliers => this.suppliers = suppliers);
  }

  save(): void {
    this.saveButtonClicked = true;
    var supplier_name = typeof this.selectedSupplier === 'object' ? this.selectedSupplier['supplierName'] : this.selectedSupplier
    var error_message = []
    // Check info
    if (supplier_name === undefined) {
      error_message.push('Please fill in supplier name');
    }
    if (!this.productName) {
      error_message.push('Please fill in product name');
    }
    if (!this.formGroup.get('selectedCategory')?.value) {
      error_message.push('Please select a category');
    }
    if (!this.formGroup.get('selectedMetal')?.value) {
      error_message.push('Please select a metal');
    }
    if (!this.formGroup.get('selectedMeasurement')?.value) {
      error_message.push('Please select a measurement');
    }

    if (error_message.length === 0) {
      const imagelinks = this.images.map(img => img.link);
      if (this.createProduct) {
        var data = {
          supplierName: supplier_name,
          productName: this.productName,
          premium: this.premium,
          category: this.formGroup.get('selectedCategory')?.value['name'],
          metal: this.formGroup.get('selectedMetal')?.value['name'],
          year: this.year,
          measurement: this.formGroup.get('selectedMeasurement')?.value['name'],
          weight: this.weight,
          quantity: this.quantity,
          images: imagelinks
        };
        this.pMetalService.addProduct(data).subscribe(() => {
          this.updateTableFunction();
          this.closeModalFunction();
          alert(this.productName + ' added');
        });
      } else {
        var dataEdit = {
          productID: this.editProduct.productID,
          supplierName: supplier_name,
          productName: this.productName,
          premium: this.premium,
          category: this.formGroup.get('selectedCategory')?.value['name'],
          metal: this.formGroup.get('selectedMetal')?.value['name'],
          year: this.year,
          measurement: this.formGroup.get('selectedMeasurement')?.value['name'],
          weight: this.weight,
          quantity: this.quantity,
          images: imagelinks
        };
        
        const nonMatchingProperties: string[] = this.compareObjects(this.initialEditProductData, dataEdit);
        const dataEditPass: any = {};

        // Loop through nonMatchingProperties array
        nonMatchingProperties.forEach(propertyName => {
          // Check if the property is not productID
          if (propertyName !== 'productID') {
            // Add the property to dataEditPass from dataEdit object
            dataEditPass[propertyName] = dataEdit[propertyName as keyof typeof dataEdit];
          }
        });


        // Add productID to dataEditPass
        dataEditPass['productID'] = dataEdit['productID'];
        dataEditPass['update_columns'] = nonMatchingProperties;

        // Output the dataEditPass object
        console.log(dataEditPass);
        console.log(this.initialEditProductData.images);

        this.pMetalService.updateProduct(dataEditPass).subscribe(() => {
          this.updateTableFunction();
          this.closeModalFunction();
          alert(this.productName + ' update');
        });
      }
    } else {
      // Display warning message
      alert(error_message.join('\n'));
    }
  }

  compareObjects(obj1: any, obj2: any): string[] {
    const nonMatchingProperties: string[] = [];

    // Iterate over the properties of obj1
    for (const key in obj1) {
      if (Object.prototype.hasOwnProperty.call(obj1, key)) {
        // Check if the property exists in obj2 and if their values match
        if (Object.prototype.hasOwnProperty.call(obj2, key) && obj1[key] !== obj2[key]) {
          nonMatchingProperties.push(key); // Add the property name to the list
        }
      }
    }

    // Iterate over the properties of obj2 that are not present in obj1
    for (const key in obj2) {
      if (Object.prototype.hasOwnProperty.call(obj2, key) && !Object.prototype.hasOwnProperty.call(obj1, key)) {
        nonMatchingProperties.push(key); // Add the property name to the list
      }
    }

    return nonMatchingProperties;
  }

  closeModalFunction(): void {
    if (this.enableEdit && !this.createProduct) {
      this.enableEditButton();
    } else {
      this.closeModal.emit();
    }
  }

  updateTableFunction(): void {
    this.updateTable.emit();
  }

  addImage(): void {
    // check if image link is inserted
    if (this.image) {
      // check if image link already exists
      if (!this.images.some(img => img.link === this.image)) {
        // add to images
        this.images.push({ link: this.image, edit: false });
        this.image = '';
      } else {
        alert('Image link already exists');
      }
    } else {
      alert('Please insert an image link');
    }
  }

  removeImage(link: string): void {
    const index = this.images.findIndex(img => img.link === link);
    if (index !== -1) {
      this.images[index].edit = true;
    }
  }


  proceedremoveImage(link: string): void {
    const index = this.images.findIndex(img => img.link === link);
    if (index !== -1) {
      this.images.splice(index, 1);
    }
  }

  cancelRemoveImage(link: string): void {
    const index = this.images.findIndex(img => img.link === link);
    if (index !== -1) {
      this.images[index].edit = false;
    }
  }
}
