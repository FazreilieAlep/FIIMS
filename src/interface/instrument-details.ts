export interface instrument_details {
  instrumentID: number;
  instrumentName: string;
  supplierName: string;
  quantity?: number;
  imageLink?: string;
  brand?: string;
  variation?: string;
  price?: number;
  delete?: boolean;
  images?: string[];
  category: string[];
  desc: string;
}
