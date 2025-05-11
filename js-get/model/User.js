module.exports = class User {
    constructor(id, name, email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    static fromItem(item) {
        return new User(item.id, item.name, item.email);
    }
}