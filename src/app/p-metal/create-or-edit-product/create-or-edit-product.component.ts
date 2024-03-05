import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-create-or-edit-product',
  templateUrl: './create-or-edit-product.component.html',
  styleUrls: ['./create-or-edit-product.component.css']
})
export class CreateOrEditProductComponent implements OnInit {

  edit: Boolean = false;
  create: Boolean = false;

  constructor(public dialogRef: MatDialogRef<CreateOrEditProductComponent>) { }

  ngOnInit(): void {
  }

  closeModal(): void {
    this.dialogRef.close();
  }

}
