from rest_framework import viewsets, generics, permissions , status
from .models import Sale
from .serializers import SaleSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Sale.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SaleListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sales = Sale.objects.filter(user=request.user)
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("Dados recebidos:", request.data)  # Log dos dados recebidos
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        print("Erros de validação:", serializer.errors)  # Log dos erros de validação
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        try:
            sale = Sale.objects.get(pk=pk, user=request.user)  # Filtra a venda pelo ID e pelo usuário autenticado
        except Sale.DoesNotExist:
            return Response({"error": "Venda não encontrada."}, status=404)

        serializer = SaleSerializer(sale, data=request.data, partial=True)  # Permite atualizações parciais
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class SaleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk, user=request.user)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class SaleView(APIView):
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados podem acessar

    def get(self, request):
        sales = Sale.objects.filter(user=request.user)  # Filtra as vendas pelo usuário autenticado
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associa a venda ao usuário autenticado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Example data for testing purposes
example_data = [
  {
    "id": 1,
    "product_line": "aves",
    "value": 1000,
    "discount_percent": 7,
    "payment_term": 120,
    "payment_dates": [
      { "month": 30, "value": 250, "paymentDate": "05/06/2025" },
      { "month": 60, "value": 250, "paymentDate": "05/07/2025" },
      { "month": 90, "value": 250, "paymentDate": "05/08/2025" },
      { "month": 120, "value": 250, "paymentDate": "05/09/2025" }
    ]
  }
]
