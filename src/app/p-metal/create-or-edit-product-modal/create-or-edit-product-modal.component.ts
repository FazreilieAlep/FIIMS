import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-create-or-edit-product-modal',
  templateUrl: './create-or-edit-product-modal.component.html',
  styleUrls: ['./create-or-edit-product-modal.component.css']
})
export class CreateOrEditProductModalComponent {
  @Input() createProduct: boolean = false;
  @Input() editProduct: boolean = false;

  @Output() closeModal = new EventEmitter<void>();

  closeModalFunction(): void {
    this.closeModal.emit();
  }

  //confirm1(event: Event) {
  //  this.confirmationService.confirm({
  //    target: event.target as EventTarget,
  //    message: 'Are you sure you want to proceed?',
  //    icon: 'pi pi-exclamation-triangle',
  //    accept: () => {
  //      this.messageService.add({ severity: 'info', summary: 'Confirmed', detail: 'You have accepted', life: 3000 });
  //    },
  //    reject: () => {
  //      this.messageService.add({ severity: 'error', summary: 'Rejected', detail: 'You have rejected', life: 3000 });
  //    }
  //  });
  //}

  //confirm2(event: Event) {
  //  this.confirmationService.confirm({
  //    target: event.target as EventTarget,
  //    message: 'Do you want to delete this record?',
  //    icon: 'pi pi-info-circle',
  //    acceptButtonStyleClass: 'p-button-danger p-button-sm',
  //    accept: () => {
  //      this.messageService.add({ severity: 'info', summary: 'Confirmed', detail: 'Record deleted', life: 3000 });
  //    },
  //    reject: () => {
  //      this.messageService.add({ severity: 'error', summary: 'Rejected', detail: 'You have rejected', life: 3000 });
  //    }
  //  });
  //}

}
