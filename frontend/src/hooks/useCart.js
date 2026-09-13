import { useMemo, useState } from "react";

export const useCart = (initialItems = [], taxRate = 0) => {
  const [cartItems, setCartItems] = useState(initialItems);
  const [isHeld, setIsHeld] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState("card");

  const updateQuantity = (id, delta) => {
    setCartItems((prevItems) =>
      prevItems
        .map((item) => {
          const newQuantity = Math.max(0, item.quantity + delta);
          return { ...item, quantity: newQuantity };
        })
        .filter((item) => item.quantity > 0)
    );
  };

  const removeItem = (id) => {
    setCartItems((prevItems) => prevItems.filter((item) => item.id !== id));
  };

  const clearCart = () => {
    setCartItems([]);
  };

  const holdBill = () => {
    setIsHeld(true);
  };

  const resumeBill = () => {
    setIsHeld(false);
  };

  const { subtotal, tax, total } = useMemo(() => {
    const rawSubtotal = cartItems.reduce(
      (sum, item) => sum + item.quantity * item.price,
      0
    );
    const computedTax = rawSubtotal * taxRate;
    return {
      subtotal: rawSubtotal,
      tax: computedTax,
      total: rawSubtotal + computedTax,
    };
  }, [cartItems, taxRate]);

  return {
    cartItems,
    setCartItems,
    isHeld,
    setIsHeld,
    holdBill,
    resumeBill,
    paymentMethod,
    setPaymentMethod,
    updateQuantity,
    removeItem,
    clearCart,
    subtotal,
    tax,
    total,
  };
};