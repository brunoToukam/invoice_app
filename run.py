from app.database import create_app
from app.routes.clients import clients_bp
from app.routes.invoices import invoices_bp
from app.routes.products import products_bp
from app.routes.tva import tva_bp

app = create_app()
app.register_blueprint(clients_bp, url_prefix='/api')
app.register_blueprint(invoices_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(tva_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
