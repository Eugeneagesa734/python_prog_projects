#!/usr/bin/env python3
"""
Enhanced Password Brute Forcer

This script provides an improved version of a password brute forcer with multiple
features including:
- Support for various character sets (numeric, alphabetic, special chars)
- Multiple attack strategies (sequential, random, mask-based)
- Performance optimizations and tracking
- User-friendly interface with progress reporting
"""

import itertools
import random
import string
import time
import argparse
from datetime import timedelta
import hashlib
import re


class PasswordBruteForcer:
    """A versatile password brute forcing utility with multiple attack strategies and options."""
    
    def __init__(self):
        # Define character sets
        self.charset_numeric = string.digits
        self.charset_lowercase = string.ascii_lowercase
        self.charset_uppercase = string.ascii_uppercase
        self.charset_special = '!@#$%^&*()-_=+[]{}|;:,.<>?/~`"\'\\' 
        
        # Track performance metrics
        self.attempts = 0
        self.start_time = None
        self.found = False
        self.result = None

    def _get_charset(self, charset_flags):
        """Build character set based on flags."""
        charset = ""
        if 'numeric' in charset_flags:
            charset += self.charset_numeric
        if 'lower' in charset_flags:
            charset += self.charset_lowercase
        if 'upper' in charset_flags:
            charset += self.charset_uppercase
        if 'special' in charset_flags:
            charset += self.charset_special
        
        # Default to numeric if no charset specified
        if not charset:
            charset = self.charset_numeric
            
        return charset

    def _check_password(self, guess, target, hash_type=None):
        """Check if the password guess matches the target."""
        self.attempts += 1
        
        # For clear text matching
        if hash_type is None:
            return guess == target
            
        # For hash matching
        if hash_type == 'md5':
            return hashlib.md5(guess.encode()).hexdigest() == target
        elif hash_type == 'sha1':
            return hashlib.sha1(guess.encode()).hexdigest() == target
        elif hash_type == 'sha256':
            return hashlib.sha256(guess.encode()).hexdigest() == target
        
        return False

    def _print_stats(self, current_guess=None, interval=0.5):
        """Print statistics about the ongoing brute force attempt."""
        elapsed = time.time() - self.start_time
        
        # Only print stats periodically to avoid overwhelming output
        if elapsed < self.last_stats_time + interval:
            return
            
        self.last_stats_time = elapsed
        
        # Calculate speed
        speed = self.attempts / elapsed if elapsed > 0 else 0
        
        # Estimate remaining time (if we know the total combinations)
        remaining_str = ""
        if hasattr(self, 'total_combinations'):
            if self.attempts < self.total_combinations:
                remaining_seconds = (self.total_combinations - self.attempts) / speed if speed > 0 else float('inf')
                remaining_str = f" | Est. remaining: {timedelta(seconds=int(remaining_seconds))}"
        
        # Create status line
        if current_guess:
            current_str = f"Current: {current_guess}"
        else:
            current_str = ""
            
        # Print status with progress percentage if available
        progress_str = ""
        if hasattr(self, 'total_combinations'):
            progress = (self.attempts / self.total_combinations) * 100
            progress_str = f"{progress:.2f}% "
            
        print(f"\r{progress_str}Attempts: {self.attempts} | Speed: {speed:.2f} p/s | Elapsed: {timedelta(seconds=int(elapsed))}{remaining_str} | {current_str}", end="")

    def sequential_attack(self, target, min_length=1, max_length=8, charset_flags=None, 
                         hash_type=None, verbose=False, max_attempts=None):
        """
        Sequential brute force attack that tries all possible combinations.
        
        Args:
            target: The password to crack or its hash
            min_length: Minimum password length to try
            max_length: Maximum password length to try
            charset_flags: List of character sets to use (numeric, lower, upper, special)
            hash_type: Type of hash to match (None, md5, sha1, sha256)
            verbose: Whether to print each attempt
            max_attempts: Maximum number of attempts before giving up
        
        Returns:
            The cracked password or None if not found
        """
        charset = self._get_charset(charset_flags or ['numeric'])
        self.start_time = time.time()
        self.last_stats_time = 0
        self.attempts = 0
        
        # Calculate total combinations for progress tracking
        self.total_combinations = sum(len(charset) ** length for length in range(min_length, max_length + 1))
        
        print(f"Starting sequential attack with character set: {charset}")
        print(f"Testing passwords of length {min_length} to {max_length}")
        print(f"Total possible combinations: {self.total_combinations:,}")
        
        for length in range(min_length, max_length + 1):
            print(f"\nTrying length: {length}")
            
            for guess_tuple in itertools.product(charset, repeat=length):
                guess = ''.join(guess_tuple)
                
                if verbose:
                    print(f"Trying: {guess}")
                elif not verbose and self.attempts % 10000 == 0:
                    self._print_stats(guess)
                
                if self._check_password(guess, target, hash_type):
                    print(f"\nPassword found: {guess}")
                    self.found = True
                    self.result = guess
                    return guess
                    
                if max_attempts and self.attempts >= max_attempts:
                    print(f"\nReached maximum attempts ({max_attempts}). Stopping.")
                    return None
        
        print("\nPassword not found.")
        return None

    def random_attack(self, target, length=4, charset_flags=None, 
                     hash_type=None, verbose=False, max_attempts=1000000):
        """
        Random brute force attack that tries random combinations.
        
        Args:
            target: The password to crack or its hash
            length: Password length to try
            charset_flags: List of character sets to use (numeric, lower, upper, special)
            hash_type: Type of hash to match (None, md5, sha1, sha256)
            verbose: Whether to print each attempt
            max_attempts: Maximum number of attempts before giving up
        
        Returns:
            The cracked password or None if not found
        """
        charset = self._get_charset(charset_flags or ['numeric'])
        self.start_time = time.time()
        self.last_stats_time = 0
        self.attempts = 0
        
        print(f"Starting random attack with character set: {charset}")
        print(f"Testing passwords of length {length}")
        print(f"Maximum attempts: {max_attempts:,}")
        
        # For random attack we use max_attempts as total_combinations for progress tracking
        self.total_combinations = max_attempts
        
        tried_passwords = set()
        
        while self.attempts < max_attempts:
            # Generate random password
            guess = ''.join(random.choice(charset) for _ in range(length))
            
            # Skip if we've already tried this password
            if guess in tried_passwords:
                continue
                
            tried_passwords.add(guess)
            
            if verbose:
                print(f"Trying: {guess}")
            elif not verbose and self.attempts % 1000 == 0:
                self._print_stats(guess)
            
            if self._check_password(guess, target, hash_type):
                print(f"\nPassword found: {guess}")
                self.found = True
                self.result = guess
                return guess
        
        print("\nPassword not found after maximum attempts.")
        return None

    def mask_attack(self, target, mask, hash_type=None, verbose=False):
        """
        Mask-based attack where parts of the password are known.
        
        Args:
            target: The password to crack or its hash
            mask: Password mask with '?' for unknown chars (e.g. '12??' means first two chars are '12')
            hash_type: Type of hash to match (None, md5, sha1, sha256)
            verbose: Whether to print each attempt
        
        Returns:
            The cracked password or None if not found
        """
        self.start_time = time.time()
        self.last_stats_time = 0
        self.attempts = 0
        
        # Find positions of unknown characters
        unknown_positions = [i for i, char in enumerate(mask) if char == '?']
        fixed_chars = list(mask)
        
        # Calculate total combinations
        self.total_combinations = 10 ** len(unknown_positions)  # Assuming numeric chars for simplicity
        
        print(f"Starting mask attack with mask: {mask}")
        print(f"Unknown positions: {len(unknown_positions)}")
        print(f"Total possible combinations: {self.total_combinations:,}")
        
        # Generate all possible combinations for unknown positions
        for combo in itertools.product(self.charset_numeric, repeat=len(unknown_positions)):
            # Fill in unknown positions with current combination
            for i, pos in enumerate(unknown_positions):
                fixed_chars[pos] = combo[i]
            
            guess = ''.join(fixed_chars)
            
            if verbose:
                print(f"Trying: {guess}")
            elif not verbose and self.attempts % 10000 == 0:
                self._print_stats(guess)
            
            if self._check_password(guess, target, hash_type):
                print(f"\nPassword found: {guess}")
                self.found = True
                self.result = guess
                return guess
        
        print("\nPassword not found.")
        return None

    def dictionary_attack(self, target, dictionary_file, hash_type=None, verbose=False):
        """
        Dictionary-based attack using a wordlist.
        
        Args:
            target: The password to crack or its hash
            dictionary_file: Path to a dictionary file with one password per line
            hash_type: Type of hash to match (None, md5, sha1, sha256)
            verbose: Whether to print each attempt
        
        Returns:
            The cracked password or None if not found
        """
        self.start_time = time.time()
        self.last_stats_time = 0
        self.attempts = 0
        
        try:
            with open(dictionary_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Count lines for progress tracking
                line_count = sum(1 for _ in f)
                f.seek(0)  # Reset file pointer to beginning
                
                self.total_combinations = line_count
                
                print(f"Starting dictionary attack using: {dictionary_file}")
                print(f"Dictionary contains {line_count:,} entries")
                
                for line in f:
                    password = line.strip()
                    
                    if verbose:
                        print(f"Trying: {password}")
                    elif not verbose and self.attempts % 1000 == 0:
                        self._print_stats(password)
                    
                    if self._check_password(password, target, hash_type):
                        print(f"\nPassword found: {password}")
                        self.found = True
                        self.result = password
                        return password
                        
            print("\nPassword not found in dictionary.")
            return None
            
        except FileNotFoundError:
            print(f"Dictionary file not found: {dictionary_file}")
            return None


def main():
    parser = argparse.ArgumentParser(description="Enhanced Password Brute Forcer")
    
    # Define attack modes
    parser.add_argument('--mode', choices=['sequential', 'random', 'mask', 'dictionary'], 
                        default='sequential', help='Attack mode')
    
    # Target password or hash
    parser.add_argument('--target', required=True, help='Target password or hash to crack')
    
    # Hash type
    parser.add_argument('--hash-type', choices=['md5', 'sha1', 'sha256'], 
                        help='Hash type if target is a hash')
    
    # Character set options
    parser.add_argument('--charset', nargs='+', choices=['numeric', 'lower', 'upper', 'special'],
                        default=['numeric'], help='Character sets to use')
    
    # Length options
    parser.add_argument('--min-length', type=int, default=1, help='Minimum password length')
    parser.add_argument('--max-length', type=int, default=8, help='Maximum password length')
    parser.add_argument('--length', type=int, help='Exact password length (overrides min/max)')
    
    # Dictionary file
    parser.add_argument('--dictionary', help='Path to dictionary file')
    
    # Mask for mask-based attack
    parser.add_argument('--mask', help='Password mask with ? for unknown chars (e.g. 12??)')
    
    # Other options
    parser.add_argument('--max-attempts', type=int, default=1000000, 
                        help='Maximum number of attempts')
    parser.add_argument('--verbose', action='store_true', help='Show all attempts')
    
    args = parser.parse_args()
    
    # Initialize the brute forcer
    brute_forcer = PasswordBruteForcer()
    
    # Set exact length if specified
    if args.length:
        args.min_length = args.length
        args.max_length = args.length
    
    # Run the appropriate attack
    if args.mode == 'sequential':
        brute_forcer.sequential_attack(
            args.target, 
            min_length=args.min_length, 
            max_length=args.max_length, 
            charset_flags=args.charset,
            hash_type=args.hash_type,
            verbose=args.verbose,
            max_attempts=args.max_attempts
        )
        
    elif args.mode == 'random':
        brute_forcer.random_attack(
            args.target,
            length=args.length or 4,
            charset_flags=args.charset,
            hash_type=args.hash_type,
            verbose=args.verbose,
            max_attempts=args.max_attempts
        )
        
    elif args.mode == 'mask':
        if not args.mask:
            print("Error: Mask attack requires --mask argument")
            return
        
        brute_forcer.mask_attack(
            args.target,
            args.mask,
            hash_type=args.hash_type,
            verbose=args.verbose
        )
        
    elif args.mode == 'dictionary':
        if not args.dictionary:
            print("Error: Dictionary attack requires --dictionary argument")
            return
            
        brute_forcer.dictionary_attack(
            args.target,
            args.dictionary,
            hash_type=args.hash_type,
            verbose=args.verbose
        )
    
    # Report final statistics
    end_time = time.time()
    elapsed = end_time - brute_forcer.start_time
    attempts = brute_forcer.attempts
    
    print("\n--- Final Report ---")
    print(f"Mode: {args.mode}")
    print(f"Total attempts: {attempts:,}")
    print(f"Time elapsed: {timedelta(seconds=int(elapsed))}")
    print(f"Average speed: {attempts / elapsed:.2f} passwords/second")
    print(f"Password {'found' if brute_forcer.found else 'not found'}")
    if brute_forcer.found:
        print(f"Password: {brute_forcer.result}")


if __name__ == "__main__":
    main()


