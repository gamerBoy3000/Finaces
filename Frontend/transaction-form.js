using System;
using System.ComponentModel.DataAnnotations;

public class Transaction
{
    // A unique identifier for the transaction.
    public int Id { get; set; }

    // The amount of the transaction. Using 'decimal' is best practice for monetary values to avoid floating-point errors.
    [Required]
    public decimal Amount { get; set; }

    // A description of the transaction.
    [Required]
    [StringLength(255)]
    public string Description { get; set; }

    // The date and time the transaction occurred.
    public DateTime Date { get; set; }

    // The category of the transaction (e.g., "Groceries", "Utilities").
    [StringLength(100)]
    public string Category { get; set; }
}