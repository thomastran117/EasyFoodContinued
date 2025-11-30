import { Component, ElementRef, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare var paypal: any;

@Component({
  selector: 'app-paypal-button',
  template: `<div id="paypal-button-container"></div>`,
})
export class PaypalButtonComponent implements AfterViewInit {
  constructor(
    private http: HttpClient,
    private el: ElementRef,
  ) {}

  ngAfterViewInit(): void {
    paypal
      .Buttons({
        createOrder: async () => {
          const res: any = await this.http
            .post('/api/payment/create', {
              order_id: 123,
              total: 49.99,
              currency: 'CAD',
            })
            .toPromise();
          return res.order_id;
        },
        onApprove: async (data: any) => {
          await this.http.post(`/api/payment/capture`, { order_id: data.orderID }).toPromise();
          alert('Payment successful!');
        },
        onCancel: () => alert('Payment cancelled'),
        onError: (err: any) => console.error('PayPal Error:', err),
      })
      .render('#paypal-button-container');
  }
}
