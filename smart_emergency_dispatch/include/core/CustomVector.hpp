#ifndef CORE_CUSTOM_VECTOR_HPP
#define CORE_CUSTOM_VECTOR_HPP

#include <cstddef>
#include <utility>
#include <stdexcept>
#include <initializer_list>

namespace Core {

/**
 * @brief Zero-STL Dynamic Array implementation guaranteeing direct algorithm ownership.
 * Fulfills the project requirement prohibiting standard template library containers for core logic.
 */
template <typename T>
class CustomVector {
private:
    T* data_;
    size_t size_;
    size_t capacity_;

    void reallocate(size_t new_capacity) {
        T* new_data = new T[new_capacity];
        for (size_t i = 0; i < size_; ++i) {
            new_data[i] = std::move(data_[i]);
        }
        delete[] data_;
        data_ = new_data;
        capacity_ = new_capacity;
    }

public:
    CustomVector() : data_(nullptr), size_(0), capacity_(0) {}

    explicit CustomVector(size_t count, const T& value = T()) : size_(count), capacity_(count) {
        data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
        for (size_t i = 0; i < size_; ++i) {
            data_[i] = value;
        }
    }

    CustomVector(std::initializer_list<T> init) : size_(init.size()), capacity_(init.size()) {
        data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
        size_t idx = 0;
        for (const auto& item : init) {
            data_[idx++] = item;
        }
    }

    ~CustomVector() {
        delete[] data_;
        data_ = nullptr;
        size_ = 0;
        capacity_ = 0;
    }

    // Copy constructor
    CustomVector(const CustomVector& other) : size_(other.size_), capacity_(other.capacity_) {
        data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
        for (size_t i = 0; i < size_; ++i) {
            data_[i] = other.data_[i];
        }
    }

    // Copy assignment
    CustomVector& operator=(const CustomVector& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            capacity_ = other.capacity_;
            data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
            for (size_t i = 0; i < size_; ++i) {
                data_[i] = other.data_[i];
            }
        }
        return *this;
    }

    // Move constructor
    CustomVector(CustomVector&& other) noexcept 
        : data_(other.data_), size_(other.size_), capacity_(other.capacity_) {
        other.data_ = nullptr;
        other.size_ = 0;
        other.capacity_ = 0;
    }

    // Move assignment
    CustomVector& operator=(CustomVector&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            capacity_ = other.capacity_;
            other.data_ = nullptr;
            other.size_ = 0;
            other.capacity_ = 0;
        }
        return *this;
    }

    void push_back(const T& value) {
        if (size_ == capacity_) {
            size_t new_cap = (capacity_ == 0) ? 2 : capacity_ * 2;
            reallocate(new_cap);
        }
        data_[size_++] = value;
    }

    void push_back(T&& value) {
        if (size_ == capacity_) {
            size_t new_cap = (capacity_ == 0) ? 2 : capacity_ * 2;
            reallocate(new_cap);
        }
        data_[size_++] = std::move(value);
    }

    void pop_back() {
        if (size_ > 0) {
            --size_;
        }
    }

    void clear() {
        size_ = 0;
    }

    void reserve(size_t new_capacity) {
        if (new_capacity > capacity_) {
            reallocate(new_capacity);
        }
    }

    void resize(size_t new_size, const T& default_val = T()) {
        if (new_size > capacity_) {
            reallocate(new_size);
        }
        for (size_t i = size_; i < new_size; ++i) {
            data_[i] = default_val;
        }
        size_ = new_size;
    }

    T& operator[](size_t index) {
        return data_[index];
    }

    const T& operator[](size_t index) const {
        return data_[index];
    }

    T& at(size_t index) {
        if (index >= size_) {
            throw std::out_of_range("CustomVector::at: index out of range");
        }
        return data_[index];
    }

    const T& at(size_t index) const {
        if (index >= size_) {
            throw std::out_of_range("CustomVector::at: index out of range");
        }
        return data_[index];
    }

    T& front() { return data_[0]; }
    const T& front() const { return data_[0]; }
    T& back() { return data_[size_ - 1]; }
    const T& back() const { return data_[size_ - 1]; }

    size_t size() const { return size_; }
    size_t capacity() const { return capacity_; }
    bool empty() const { return size_ == 0; }

    T* data() { return data_; }
    const T* data() const { return data_; }

    T* begin() { return data_; }
    const T* begin() const { return data_; }
    T* end() { return data_ + size_; }
    const T* end() const { return data_ + size_; }
};

} // namespace Core

#endif // CORE_CUSTOM_VECTOR_HPP
